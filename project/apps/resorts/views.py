from django.utils.translation import ugettext as _
from rest_framework import mixins, generics
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
import urllib
import json
from apps.asset.models import Assets
from apps.authentication.custom_permission_drf import AssetAccessPermission
from apps.controlled_substance.models import Stock, IN, OUT
from apps.custom_user.utils import get_roleid_user
from apps.resorts.models import Area
from apps.resorts.models import DELETED
from apps.resorts.models import LIVE
from apps.resorts.models import Resort
from apps.resorts.models import ResortLocation
from apps.resorts.models import UserResortMap
from apps.resorts.serializers import AreaSerializer
from apps.resorts.serializers import LocationSerializer
from apps.resorts.serializers import ResortSerializer
from apps.resorts.utils import get_resort_for_user, transform_resort_settings_request
from apps.resorts.utils import get_setting_data_for_resort
from apps.resorts.utils import get_userrole_for_resort


class ResortViewSet(ViewSet, mixins.ListModelMixin, generics.GenericAPIView):
    def create(self, request):
        user = request.user

        if user.is_admin:
            resort_data = request.data
            resort_serialized_data = ResortSerializer(data=resort_data)

            if resort_serialized_data.is_valid():
                resort = resort_serialized_data.save()
                response_resort_data = ResortSerializer(resort, fields=('resort_id', 'resort_name', 'map_kml',
                                                                        'map_type', 'location', 'print_on_device',
                                                                        'map_lat', 'map_lng', 'network_key',
                                                                        'license_expiry_date', 'licenses',
                                                                        'report_form', 'website', 'domain_id',
                                                                        'unit_format', 'timezone', 'resort_logo',
                                                                        'datetime_format',
                                                                        'resort_controlled_substances',
                                                                        'resort_asset_management'))
                return Response(response_resort_data.data, status=200)
            else:
                return Response(resort_serialized_data.errors, status=400)
        else:
            return Response({_('detail'): _("You dont have the permission to create resort")}, status=403)

    def update(self, request, pk=None):
        user = request.user
        resort = Resort.objects.filter(resort_id=pk).first()

        if resort is not None:
            if user.is_admin:
                resort_data = request.data
                resort_serialized_data = ResortSerializer(resort, data=resort_data, partial=True)
                resort_data.pop('network_key', None)

                if resort_serialized_data.is_valid():
                    resort = resort_serialized_data.save()
                    response_resort_data = ResortSerializer(resort, fields=('resort_id', 'resort_name', 'map_kml',
                                                                            'map_type', 'location', 'print_on_device',
                                                                            'map_lat', 'map_lng', 'network_key',
                                                                            'license_expiry_date', 'licenses',
                                                                            'report_form', 'website', 'domain_id',
                                                                            'unit_format', 'timezone', 'resort_logo',
                                                                            'dispatch_field_choice',
                                                                            'datetime_format',
                                                                            'resort_controlled_substances',
                                                                            'resort_asset_management'), partial=True)
                    return Response(response_resort_data.data, status=200)
                else:
                    return Response(resort_serialized_data.errors, status=400)
            else:
                return Response({_('detail'): _("You dont have the permission to update resort")}, status=403)
        else:
            return Response({_("detail"): _("Resort does not exists")}, status=400)

    def retrieve(self, request, pk=None):
        resort = Resort.objects.filter(resort_id=pk).first()
        response_data = []

        if resort is not None:
            try:
                user_resort = UserResortMap.objects.get(user=request.user, resort=resort)
            except:
                return Response({_('detail'): _('You dont have the permission to get resort information')}, status=403)

            resort_data = ResortSerializer(resort, fields=('resort_id', 'resort_name', 'map_kml',
                                                           'map_type', 'location', 'print_on_device',
                                                           'map_lat', 'map_lng', 'network_key',
                                                           'license_expiry_date', 'licenses',
                                                           'report_form', 'website', 'domain_id',
                                                           'unit_format', 'timezone', 'resort_logo',
                                                           'dispatch_field_choice', 'datetime_format',
                                                           'resort_controlled_substances', 'resort_asset_management'))
            user_data = get_userrole_for_resort(resort=resort, method='get', user=request.user)

            response_data = resort_data.data
            response_data['users'] = user_data
            return Response(response_data, status=200)
        else:
            return Response({_("detail"): _("Resort does not exists")}, status=400)

    def list(self, request, *args, **kwargs):
        user = self.request.user
        resort_name = request.query_params.get('resort_name')

        if user.is_admin:
            if resort_name is not None:
                query = Resort.objects.filter(resort_name__icontains=resort_name)
            else:
                query = Resort.objects.all()

        else:
            user_resorts = UserResortMap.objects.filter(user=user).values('resort')
            resort_id = []
            if user_resorts != 0:
                for user_resort in user_resorts:
                    resort_id.append(user_resort['resort'])

                if resort_name is not None:
                    query = Resort.objects.filter(pk__in=resort_id).filter(resort_name__icontains=resort_name)
                else:
                    query = Resort.objects.filter(pk__in=resort_id)

        queryset = self.filter_queryset(query)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ResortSerializer(page, fields=('resort_name', 'map_kml', 'map_type',
                                                        'location', 'print_on_device', 'map_lat',
                                                        'map_lng', 'network_key', 'license_expiry_date', 'licenses',
                                                        'report_form', 'website', 'unit_format',
                                                        'timezone', 'resort_logo', 'datetime_format',
                                                        'resort_controlled_substances',
                                                        'resort_asset_management'), many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @detail_route()
    def users(self, request, pk=None):
        user = request.user
        resort = Resort.objects.filter(resort_id=pk).first()
        response_data = {}

        if resort is not None:
            try:
                user_resort = UserResortMap.objects.get(user=request.user, resort=resort)
            except:
                return Response({_('detail'): _('You dont have the permission to get user for the resort')}, status=403)

            user_data = get_userrole_for_resort(resort=resort, method='list', user=request.user)
            response_data['users'] = user_data
            response_data['user_count'] = len(user_data)
            response_data['resort_id'] = resort.resort_id
            return Response(response_data, status=200)
        else:
            return Response({"detail": "Resort does not exists"}, status=400)

    @detail_route(methods=['GET', 'PUT'], url_path='settings')
    def resort_setting(self, request, pk=None):
        return_data = {}
        user = request.user

        try:
            resort = Resort.objects.get(resort_id=pk)
        except:
            return Response({_('detail'): _('no resort associated with user')}, status=400)

        if request.method == 'PUT':
            role = get_roleid_user(resort=resort, user=user)
            if role != 3:
                return Response({_('detail'): _('you do not have permission to resource')}, status=400)

        if request.method == 'GET':
            return_data = get_setting_data_for_resort(resort=resort)
        elif request.method == 'PUT':
            data = transform_resort_settings_request(request.data)
            resort_serialized_data = ResortSerializer(resort, data=data, partial=True)

            if resort_serialized_data.is_valid():
                resort = resort_serialized_data.save()
            else:
                return Response(resort_serialized_data.errors, status=400)

            return_data = get_setting_data_for_resort(resort=resort)
        if "map_kml" in return_data and return_data["map_kml"]:
            try:
                return_data["geojson"] = json.loads(open(urllib.urlretrieve(return_data["map_kml"])[0]).read())
            except:
                pass
        return Response(return_data, status=200)


class AreaViewSet(ViewSet, mixins.ListModelMixin, generics.GenericAPIView):
    permission_classes = [IsAuthenticated, AssetAccessPermission]

    def create(self, request):
        resort = get_resort_for_user(request.user)

        area_data = AreaSerializer(data=request.data, fields=('area_name',))

        if area_data.is_valid():
            area = area_data.save(resort=resort)
        else:
            return Response(area_data.errors, status=400)

        return Response(AreaSerializer(area, fields=('area_id', 'area_name')).data, status=200)

    def update(self, request, pk=None):

        try:
            area = Area.objects.get(area_id=pk)
        except:
            return Response({_('detail'): _('area not found')}, status=400)

        if area.area_status == DELETED:
            return Response({_('detail'): _('area not found')}, status=400)

        area_data = AreaSerializer(area, data=request.data, fields=('area_name',))

        if area_data.is_valid():
            area = area_data.save()
        else:
            return Response(area_data.errors, status=400)

        return Response(AreaSerializer(area, fields=('area_id', 'area_name')).data, status=200)

    def retrieve(self, request, pk=None):
        resort = get_resort_for_user(request.user)
        try:
            area = Area.objects.get(area_id=pk)
            if area.area_status == DELETED:
                return Response({_('detail'): _('area not found')}, status=400)
        except:
            return Response({_('detail'): _('area not found')}, status=400)

        return Response(AreaSerializer(area, fields=('area_id', 'area_name'),
                                       context={'location_count': True, 'resort': resort}).data, status=200)

    def destroy(self, request, pk=None):
        try:
            area = Area.objects.get(area_id=pk)
            locations = ResortLocation.objects.filter(area=area, location_status=LIVE)
            if not locations:
                if area.area_status == DELETED:
                    return Response({_('detail'): _('area not found')}, status=400)
            else:
                return Response(
                    {_('detail'): _('area can not be deleted because it is associated with other location')},
                    status=400)
        except:
            return Response({_('detail'): _('area not found')}, status=400)

        area.area_status = DELETED
        area.save()

        return Response({
            "area_id": area.area_id,
            "status": "deleted"
        }, status=200)

    def list(self, request, *args, **kwargs):
        resort = get_resort_for_user(request.user)
        search = request.query_params.get('search', '')
        order_by = request.query_params.get('order_by', 'area_name')
        order_by_direction = request.query_params.get('order_by_direction', 'desc')

        if order_by_direction == 'desc':
            order = '-' + order_by
        elif order_by_direction == 'asc':
            order = order_by

        query = Area.objects.filter(area_name__icontains=search, resort=resort, area_status=LIVE).order_by(order)
        queryset = self.filter_queryset(query)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AreaSerializer(page, fields=('area_id', 'area_name'), many=True,
                                        context={'location_count': True, 'resort': resort})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class LocationViewSet(ViewSet, mixins.ListModelMixin, generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        resort = get_resort_for_user(request.user)
        area_id = request.data.get('area_id', '')

        if area_id:
            try:
                area = Area.objects.get(area_id=area_id)
                if area.area_status == DELETED:
                    return Response({_('detail'): _('area not found')}, status=400)
            except:
                return Response({_('detail'): _('area not found')}, status=400)
        else:
            return Response({_('detail'): _('area_id not provided')}, status=400)

        location_data = LocationSerializer(data=request.data, fields=('location_name', 'map_lat', 'map_long'))

        if location_data.is_valid():
            location = location_data.save(area=area, resort=resort)
        else:
            return Response(location_data.errors, status=400)

        return Response(LocationSerializer(location).data, status=200)

    def update(self, request, pk=None):

        try:
            location = ResortLocation.objects.get(location_id=pk)
            if location.location_status == DELETED:
                return Response({_('detail'): _('location not found')}, status=400)
        except:
            return Response({_('detail'): _('location not found')}, status=400)

        area_id = request.data.get('area_id', '')
        area = None

        if area_id:
            try:
                area = Area.objects.get(area_id=area_id)
                if area.area_status == DELETED:
                    return Response({_('detail'): _('area not found')}, status=400)
            except:
                return Response({_('detail'): _('area not found')}, status=400)

        location_data = LocationSerializer(location, data=request.data, fields=('location_name', 'map_lat', 'map_long'))

        if location_data.is_valid():
            if area is not None:
                location = location_data.save(area=area)
            else:
                location = location_data.save()
        else:
            return Response(location_data.errors, status=400)

        return Response(LocationSerializer(location).data, status=200)

    def retrieve(self, request, pk=None):
        try:
            location = ResortLocation.objects.get(location_id=pk)
            if location.location_status == DELETED:
                return Response({_('detail'): _('location not found')}, status=400)
        except:
            return Response({_('detail'): _('location not found')}, status=400)

        return Response(LocationSerializer(location).data, status=200)

    def destroy(self, request, pk=None):
        try:
            location = ResortLocation.objects.get(location_id=pk)

            stocks = Stock.objects.filter(location=location, current_status__in=[IN, OUT])
            assets = Assets.objects.filter(location=location, asset_status=LIVE)

            if (not stocks) and (not assets):
                if location.location_status == DELETED:
                    return Response({_('detail'): _('location not found')}, status=400)
            else:
                if stocks and assets:
                    return Response(
                        {_('detail'): _('location can not be deleted as stock and asset is attached to it')},
                        status=400)
                elif stocks:
                    return Response({_('detail'): _('location can not be deleted as stock is attached to it')},
                                    status=400)
                elif assets:
                    return Response({_('detail'): _('location can not be deleted as asset is attached to it')},
                                    status=400)
        except:
            return Response({_('detail'): _('location not found')}, status=400)

        location.location_status = DELETED
        location.save()

        return Response({
            "location_id": location.location_id,
            "status": "deleted"
        }, status=200)

    def list(self, request, *args, **kwargs):
        resort = get_resort_for_user(request.user)
        search = request.query_params.get('search', '')
        area_id = request.query_params.get('area_id', '')
        order_by = request.query_params.get('order_by', 'location_name')
        order_by_direction = request.query_params.get('order_by_direction', 'desc')

        if order_by_direction == 'desc':
            order = '-' + order_by
        elif order_by_direction == 'asc':
            order = order_by

        if area_id:
            query = ResortLocation.objects.filter(location_name__icontains=search, resort=resort, location_status=LIVE,
                                                  area__area_id=area_id).order_by(order)
        else:
            query = ResortLocation.objects.filter(location_name__icontains=search, resort=resort,
                                                  location_status=LIVE).order_by(order)
        queryset = self.filter_queryset(query)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = LocationSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
