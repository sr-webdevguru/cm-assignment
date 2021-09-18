import datetime

from django.contrib.auth import get_user_model
from django.db import connection
from django.utils import timezone
from django.utils.translation import ugettext as _
from rest_framework import mixins, generics
from rest_framework.decorators import list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.authentication.custom_permission_drf import ControlledSubstancesAccessPermission
from apps.controlled_substance.models import AuditLog
from apps.controlled_substance.models import ControlledSubstances, DELETED, LIVE
from apps.controlled_substance.models import DISPOSED, IN, OUT, USED
from apps.controlled_substance.models import Stock
from apps.controlled_substance.models import StockAssignment
from apps.controlled_substance.serializers import AuditLogSerializer
from apps.controlled_substance.serializers import ControlledSubstancesSerializer
from apps.controlled_substance.serializers import StockAssignmentSerializer
from apps.controlled_substance.serializers import StockReportSerializer
from apps.controlled_substance.serializers import StockSerializer
from apps.controlled_substance.utils import add_log
from apps.controlled_substance.utils import remove_stock_entry_from_config, add_stock_entry_to_config
from apps.controlled_substance.utils import stock_status_count
from apps.incidents.utils import dictfetchall
from apps.resorts.models import ResortLocation
from apps.resorts.utils import get_resort_for_user

STATUS = {
    'in': 0,
    'out': 1,
    'used': 2,
    'disposed': 3
}


class ControlledSubstancesViewSet(ViewSet, mixins.ListModelMixin, generics.GenericAPIView):
    permission_classes = [IsAuthenticated, ControlledSubstancesAccessPermission]

    def create(self, request):
        resort = get_resort_for_user(request.user)
        units = request.data.get('units', '')

        controlledsubstances_data = ControlledSubstancesSerializer(data=request.data,
                                                                   fields=('controlled_substance_name', 'units'))

        if controlledsubstances_data.is_valid():
            controlledsubstances = controlledsubstances_data.save(resort=resort)
        else:
            return Response(controlledsubstances_data.errors, status=400)

        return Response(ControlledSubstancesSerializer(controlledsubstances,
                                                       fields=('controlled_substance_id', 'controlled_substance_name',
                                                               'units')).data, status=200)

    def update(self, request, pk=None):

        try:
            controlledsubstances = ControlledSubstances.objects.get(controlled_substance_id=pk)
            if controlledsubstances.controlled_substance_status == DELETED:
                return Response({_('detail'): _('controlledsubstances not found')}, status=400)
        except:
            return Response({_('detail'): _('controlledsubstances not found')}, status=400)

        controlledsubstances_data = ControlledSubstancesSerializer(controlledsubstances, data=request.data,
                                                                   fields=('controlled_substance_name', 'units'))

        if controlledsubstances_data.is_valid():
            controlledsubstances = controlledsubstances_data.save()
        else:
            return Response(controlledsubstances_data.errors, status=400)

        return Response(ControlledSubstancesSerializer(controlledsubstances,
                                                       fields=('controlled_substance_id', 'controlled_substance_name',
                                                               'units')).data, status=200)

    def retrieve(self, request, pk=None):

        try:
            controlledsubstances = ControlledSubstances.objects.get(controlled_substance_id=pk)
            if controlledsubstances.controlled_substance_status == DELETED:
                return Response({_('detail'): _('controlledsubstances not found')}, status=400)
        except:
            return Response({_('detail'): _('controlledsubstances not found')}, status=400)

        return Response(ControlledSubstancesSerializer(controlledsubstances,
                                                       fields=('controlled_substance_id', 'controlled_substance_name',
                                                               'units')).data, status=200)

    def destroy(self, request, pk=None):
        try:
            controlledsubstances = ControlledSubstances.objects.get(controlled_substance_id=pk)
            stocks = Stock.objects.filter(controlled_substance=controlledsubstances, current_status__in=[IN, OUT])
            if not stocks:
                if controlledsubstances.controlled_substance_status == DELETED:
                    return Response({_('detail'): _('controlledsubstances not found')}, status=400)
            else:
                return Response({_('detail'): _(
                    'controlled_substance can not be deleted because stock has been checked in or checked out with it')},
                                status=400)
        except:
            return Response({_('detail'): _('controlledsubstances not found')}, status=400)

        controlledsubstances.controlled_substance_status = DELETED
        controlledsubstances.save()

        return Response({
            "asset_id": controlledsubstances.controlled_substance_id,
            "status": "deleted"
        }, status=200)

    def list(self, request, *args, **kwargs):
        resort = get_resort_for_user(request.user)
        search = request.query_params.get('search', '')
        order_by = request.query_params.get('order_by', 'controlled_substance_name')
        order_by_direction = request.query_params.get('order_by_direction', 'desc')

        if order_by_direction == 'desc':
            order = '-' + order_by
        elif order_by_direction == 'asc':
            order = order_by

        query = ControlledSubstances.objects.filter(controlled_substance_name__icontains=search, resort=resort,
                                                    controlled_substance_status=LIVE).order_by(order)

        queryset = self.filter_queryset(query)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ControlledSubstancesSerializer(page, many=True, fields=('controlled_substance_id',
                                                                                 'controlled_substance_name', 'units'))
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @list_route(methods=['post'])
    def add(self, request):
        resort = get_resort_for_user(request.user)
        controlled_substance_id = request.data.get('controlled_substance_id', '')
        location_id = request.data.get('location_id', '')
        quantity = request.data.get('quantity', '')
        stocks = []

        if not quantity:
            return Response({_('detail'): _('quantity not provided')}, status=400)

        if controlled_substance_id:
            try:
                controlled_substance = ControlledSubstances.objects.get(controlled_substance_id=controlled_substance_id)
            except:
                return Response({_('detail'): _('controlled_substance not found')}, status=400)
        else:
            return Response({_('detail'): _('controlled_substance_id not provided')}, status=400)

        if location_id:
            try:
                location = ResortLocation.objects.get(location_id=location_id)
            except:
                return Response({_('detail'): _('location not found')}, status=400)
        else:
            return Response({_('detail'): _('location_id not provided')}, status=400)

        stock_data = StockSerializer(data=request.data, fields=('volume', 'dt_expiry'))

        if stock_data.is_valid():
            merged_data = {}

            try:
                dt_expiry = datetime.datetime.strptime(stock_data.data['dt_expiry'], "%Y-%m-%d %H:%M:%S")
            except:
                dt_expiry = None

            merged_data.update({'added_by_user': request.user, 'controlled_substance': controlled_substance,
                                'location': location, 'dt_expiry': dt_expiry, 'volume': stock_data.data.get('volume')})

            for i in range(0, quantity):
                temp_stock = Stock(**merged_data)
                temp_stock.save()
                stocks.append(temp_stock)
        else:
            return Response(stock_data.errors, status=400)

        log_entry = 'Qty ' + str(quantity) + ' x ' + str(stocks[0].volume) + ' ' + controlled_substance.units + ' of ' + \
                    controlled_substance.controlled_substance_name + ' ' + 'was added to stock at ' + \
                    location.location_name
        add_log(log_entry=log_entry, resort=resort, user=request.user)
        return Response(StockSerializer(stocks, fields=('controlled_substance_stock_pk', 'controlled_substance_stock_id'
                                                        , 'controlled_substance', 'location', 'volume', 'dt_expiry',
                                                        'added_by_user', 'disposed_by_user'), many=True).data,
                        status=200)

    @list_route(methods=['post'])
    def dispose(self, request):
        resort = get_resort_for_user(request.user)
        controlled_substance_stock_id = request.data.get('controlled_substance_stock_id', '')

        if not controlled_substance_stock_id:
            return Response({_('detail'): _('controlled_substances_stock_id not provided')}, status=400)

        try:
            stock = Stock.objects.get(controlled_substance_stock_id=controlled_substance_stock_id)
            controlled_substance = stock.controlled_substance
        except:
            return Response({_('detail'): _('controlled_substance_stock not found')}, status=400)

        if stock.current_status == DISPOSED:
            return Response({_('detail'): _('controlled_substance_stock has already been disposed')}, status=400)
        elif stock.current_status == IN:
            stock.disposed_by_user = request.user
            stock.dt_disposed = timezone.now()
            stock.current_status = DISPOSED
            stock.save()
        elif stock.current_status == OUT:
            return Response({_('detail'): _('this item is checked out to a user and cannot be disposed')}, status=400)
        elif stock.current_status == USED:
            return Response({_('detail'): _('this item has been used and cannot be disposed')}, status=400)

        log_entry = 'Item ' + str(stock.controlled_substance_stock_pk) + ': ' + str(stock.volume) + ' ' + \
                    controlled_substance.units + ' of ' + controlled_substance.controlled_substance_name + ' ' + \
                    'was disposed from ' + stock.location.location_name
        add_log(log_entry=log_entry, resort=resort, user=request.user)

        return Response(StockSerializer(stock, fields=('controlled_substance_stock_id', 'controlled_substance',
                                                       'location', 'volume', 'dt_expiry', 'added_by_user',
                                                       'disposed_by_user', 'dt_disposed', 'dt_added',
                                                       'controlled_substance_stock_pk')).data, status=200)

    @list_route(methods=['post'])
    def checkout(self, request):
        resort = get_resort_for_user(request.user)
        controlled_substance_stock_id = request.data.get('controlled_substance_stock_id', '')
        user_id = request.data.get('user_id', '')

        if not controlled_substance_stock_id:
            return Response({_('detail'): _('controlled_substance_stock_id not provided')}, status=400)

        try:
            stock = Stock.objects.get(controlled_substance_stock_id=controlled_substance_stock_id)
            controlled_substance = stock.controlled_substance
        except:
            return Response({_('detail'): _('controlled_substance_stock not found')}, status=400)

        if not user_id:
            return Response({_('detail'): _('user_id not provided')}, status=400)

        try:
            user = get_user_model().objects.get(user_id=user_id)
        except:
            return Response({_('detail'): _('user not found')}, status=400)

        if stock.current_status == DISPOSED:
            return Response({_('detail'): _('this item has been disposed and can not be checkout')}, status=400)
        elif stock.current_status == IN:
            stock.current_status = OUT
            stock.save()
            try:
                stock_assignment = StockAssignment.objects.get(controlled_substance_stock=stock)
                stock_assignment.controlled_substance_stock_assignment_status = OUT
                stock_assignment.user = user
            except:
                stock_assignment = StockAssignment(controlled_substance_stock=stock, user=user,
                                                   controlled_substance_stock_assignment_status=OUT)
            stock_assignment.save()
        elif stock.current_status == OUT:
            return Response({_('detail'): _('this item is already checked out to a user')}, status=400)
        elif stock.current_status == USED:
            return Response({_('detail'): _('this item has been used and cannot be checkout')}, status=400)

        # Add stock entry to the config
        status, message = add_stock_entry_to_config(resort, stock, user)

        if not status:
            return Response({_('detail'): _(message)}, status=400)

        log_entry = 'Item ' + str(stock.controlled_substance_stock_pk) + ': ' + \
                    str(stock.volume) + ' ' + controlled_substance.units + ' of ' + \
                    controlled_substance.controlled_substance_name + ' ' + 'was checked-out from ' + \
                    stock.location.location_name + ' to ' + user.name
        add_log(log_entry=log_entry, resort=resort, user=request.user)

        return Response(StockAssignmentSerializer(stock_assignment, fields=('controlled_substance_stock_assignment_id',
                                                                            'user')).data, status=200)

    @list_route(methods=['post'])
    def checkin(self, request):
        resort = get_resort_for_user(request.user)
        controlled_substance_stock_assignment_id = request.data.get('controlled_substance_stock_assignment_id', '')
        location_id = request.data.get('location_id', '')

        if not controlled_substance_stock_assignment_id:
            return Response({_('detail'): _('controlled_substances_stock_assignment_id not provided')}, status=400)

        try:
            stock_assignment = StockAssignment.objects.get(
                controlled_substance_stock_assignment_id=controlled_substance_stock_assignment_id)
            stock = stock_assignment.controlled_substance_stock
            controlled_substance = stock.controlled_substance
        except:
            return Response({_('detail'): _('controlled_substance_stock not found')}, status=400)

        location = None
        if location_id:
            try:
                location = ResortLocation.objects.get(location_id=location_id)
            except:
                return Response({_('detail'): _('location not found')}, status=400)

        if stock.current_status == DISPOSED:
            return Response({_('detail'): _('this item has been disposed and can not be checked in')}, status=400)
        elif stock.current_status == IN:
            return Response({_('detail'): _('this item is already checked in')}, status=400)
        elif stock.current_status == OUT:
            stock.current_status = IN
            if location is not None:
                stock.location = location
            stock.save()
            stock_assignment.controlled_substance_stock_assignment_status = IN
            stock_assignment.save()
        elif stock.current_status == USED:
            return Response({_('detail'): _('this item has been used and cannot be checked in')}, status=400)

        # Remove stock entry from the config
        status, message = remove_stock_entry_from_config(resort, stock)

        if not status:
            return Response({_('detail'): _(message)}, status=400)

        log_entry = 'Item ' + str(stock.controlled_substance_stock_pk) + ': ' + \
                    str(stock.volume) + ' ' + controlled_substance.units + ' of ' + \
                    controlled_substance.controlled_substance_name + ' ' + 'was checked-in to ' + \
                    stock.location.location_name + ' from ' + stock_assignment.user.name
        add_log(log_entry=log_entry, resort=resort, user=request.user)

        return Response(StockAssignmentSerializer(stock_assignment,
                                                  fields=('controlled_substance_stock_assignment_id',
                                                          'controlled_substance_stock_assignment_status')).data,
                        status=200)

    @list_route(methods=['post'])
    def relocate(self, request):
        resort = get_resort_for_user(request.user)
        controlled_substance_stock_id = request.data.get('controlled_substance_stock_id', '')
        location_id = request.data.get('location_id', '')

        if not controlled_substance_stock_id:
            return Response({_('detail'): _('controlled_substances_stock_id not provided')}, status=400)

        try:
            stock = Stock.objects.get(controlled_substance_stock_id=controlled_substance_stock_id)
            controlled_substance = stock.controlled_substance
        except:
            return Response({_('detail'): _('controlled_substance_stock not found')}, status=400)

        if not location_id:
            return Response({_('detail'): _('location_id not provided')}, status=400)

        try:
            location = ResortLocation.objects.get(location_id=location_id)
        except:
            return Response({_('detail'): _('location not found')}, status=400)

        if stock.current_status == DISPOSED:
            return Response({_('detail'): _('this item has been disposed and can not be relocated')}, status=400)
        elif stock.current_status == IN:
            stock.location = location
            stock.save()
        elif stock.current_status == OUT:
            return Response({_('detail'): _('this item is checked out. Must be checked in for relocation')}, status=400)
        elif stock.current_status == USED:
            return Response({_('detail'): _('this item has been used and cannot be relocated')}, status=400)

        log_entry = 'Item ' + str(stock.controlled_substance_stock_pk) + ': ' + \
                    str(stock.volume) + ' ' + controlled_substance.units + ' of ' + \
                    controlled_substance.controlled_substance_name + ' ' + 'relocated to ' + location.location_name
        add_log(log_entry=log_entry, resort=resort, user=request.user)

        return Response(StockSerializer(stock, fields=('controlled_substance_stock_pk',
                                                       'controlled_substance_stock_id', 'controlled_substance',
                                                       'location', 'volume', 'dt_expiry', 'added_by_user',
                                                       'disposed_by_user', 'dt_disposed', 'dt_added')).data, status=200)

    @list_route(methods=['get'])
    def report(self, request):
        resort = get_resort_for_user(request.user)
        order_by = request.query_params.get('order_by', 'controlled_substance__controlled_substance_name')
        order_by_direction = request.query_params.get('order_by_direction', 'desc')
        current_status = request.query_params.get('current_status', '')
        location_id = request.query_params.get('location_id', '')
        controlled_substance_id = request.query_params.get('controlled_substance_id', '')

        if order_by_direction == 'desc':
            order = '-' + order_by
        elif order_by_direction == 'asc':
            order = order_by

        if current_status == 'used':
            where_query = ""
            try:
                if location_id:
                    location = ResortLocation.objects.get(location_id=location_id)
                else:
                    location = None
            except:
                return Response({_('detail'): _('location not found')})

            try:
                if controlled_substance_id:
                    controlled_substance = ControlledSubstances.objects.get(
                        controlled_substance_id=controlled_substance_id)
                else:
                    controlled_substance = None
            except:
                return Response({_('detail'): _('controlled_substance not found')})

            # Create extended where query
            if location is not None:
                where_query += ' AND controlled_substance_stock.location = ' + str(location.location_pk)
            if controlled_substance is not None:
                where_query += ' AND controlled_substance_controlledsubstances.controlled_substance_pk = ' + str(
                    controlled_substance.controlled_substance_pk)

            dateFrom = request.GET.get('date_from', None)

            if dateFrom is None:
                dateFrom = datetime.datetime.today() - datetime.timedelta(days=30)
                dateFrom = dateFrom.strftime("%Y-%m-%d 00:00:00")
            else:
                dateFrom = (datetime.datetime.strptime(dateFrom, "%Y-%m-%d %H:%M:%S"))
                dateFrom = dateFrom.strftime("%Y-%m-%d 00:00:00")

            dateTo = request.GET.get('date_to', None)
            if dateTo is None:
                dateTo = datetime.datetime.today()
                dateTo = dateTo.strftime("%Y-%m-%d 23:59:59")
            else:
                dateTo = (datetime.datetime.strptime(dateTo, "%Y-%m-%d %H:%M:%S"))
                dateTo = dateTo.strftime("%Y-%m-%d 23:59:59")

            with connection.cursor() as cursor:
                cursor.execute("""SELECT array_agg(controlled_substance_stockassignment.controlled_substance_stock) as pk
FROM controlled_substance_stockassignment
INNER JOIN controlled_substance_stock ON controlled_substance_stockassignment.controlled_substance_stock = controlled_substance_stock.controlled_substance_stock_pk
INNER JOIN controlled_substance_controlledsubstances ON controlled_substance_stock.controlled_substance = controlled_substance_controlledsubstances.controlled_substance_pk
WHERE controlled_substance_controlledsubstances.resort = %d AND controlled_substance_stockassignment.dt_used >= '%s' AND controlled_substance_stockassignment.dt_used <= '%s' AND controlled_substance_stockassignment.controlled_substance_stock_assignment_status = 2%s;""" % (
                resort.resort_pk, dateFrom, dateTo, where_query))

                data = dictfetchall(cursor)
            query = Stock.objects.filter(
                controlled_substance_stock_pk__in=data[0]['pk'] if data[0]['pk'] is not None else []).exclude(
                current_status=DISPOSED).order_by(order)
        else:
            extra_conditions = {}
            if current_status:
                extra_conditions.update({"current_status": STATUS[current_status]})
            if location_id:
                extra_conditions.update({"location__location_id": location_id})
            if controlled_substance_id:
                extra_conditions.update({"controlled_substance__controlled_substance_id": controlled_substance_id})
            query = Stock.objects.filter(controlled_substance__resort=resort, **extra_conditions).exclude(
                current_status=DISPOSED).order_by(order)

        queryset = self.filter_queryset(query)

        page = self.paginate_queryset(queryset)
        if page is not None:
            stocks = Stock.objects.filter(controlled_substance__resort=resort,
                                          controlled_substance__controlled_substance_id=controlled_substance_id).exclude(
                current_status=DISPOSED)
            stock_status = stock_status_count(stocks)

            serializer = StockReportSerializer(page, many=True, fields=(
            'controlled_substance_stock_pk', 'controlled_substance_stock_id', 'controlled_substance',
            'location', 'volume', 'dt_expiry', 'added_by_user',
            'disposed_by_user'))
            response = self.get_paginated_response(serializer.data)
            response.data.update({"summary": stock_status})
            return response


class AuditLogViewSet(ViewSet, mixins.ListModelMixin, generics.GenericAPIView):
    permission_classes = [IsAuthenticated, ControlledSubstancesAccessPermission]

    def create(self, request):
        resort = get_resort_for_user(request.user)
        user = request.user
        log_entry = request.data.get('log_entry', '')

        if log_entry:
            audit_log = AuditLog(log_entry=log_entry, resort=resort, added_by_user=user)
            audit_log.save()
        else:
            return Response({_('detail'): _('log_entry can not be empty')}, status=400)

        return Response(AuditLogSerializer(audit_log, fields=('controlled_substance_audit_log_id', 'log_entry',
                                                              'dt_added', 'added_by_user')).data, status=200)

    def list(self, request, *args, **kwargs):
        resort = get_resort_for_user(request.user)
        order_by = request.query_params.get('order_by', 'dt_added')
        order_by_direction = request.query_params.get('order_by_direction', 'desc')

        if order_by_direction == 'desc':
            order = '-' + order_by
        elif order_by_direction == 'asc':
            order = order_by

        dateFrom = request.GET.get('date_from', None)

        if dateFrom is None:
            dateFrom = datetime.datetime.today() - datetime.timedelta(days=30)
        else:
            dateFrom = (datetime.datetime.strptime(dateFrom, "%Y-%m-%d %H:%M:%S"))

        dateTo = request.GET.get('date_to', None)
        if dateTo is None:
            dateTo = datetime.datetime.today()
        else:
            dateTo = datetime.datetime.strptime(dateTo, "%Y-%m-%d %H:%M:%S")

        query = AuditLog.objects.filter(resort=resort, dt_added__gte=dateFrom, dt_added__lte=dateTo).order_by(order)

        queryset = self.filter_queryset(query)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AuditLogSerializer(page, many=True, fields=('controlled_substance_audit_log_id', 'log_entry',
                                                                     'dt_added', 'added_by_user'))
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, fields=('controlled_substance_audit_log_id', 'log_entry',
                                                                      'dt_added', 'added_by_user'))
        return Response(serializer.data)
