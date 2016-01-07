from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.utils.translation import ugettext as _
from rest_framework.decorators import detail_route, api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from validators import uuid

from apps.authentication.custom_authentication_drf import OauthAuthentication
from apps.authentication.custom_authentication_drf import TokenAuthentication, SessionAuthentication
from apps.data_sync.models import Language
from apps.devices.models import Devices
from apps.devices.models import Heartbeat
from apps.devices.serializers import DeviceSerializer
from apps.incidents.models import Incident, StatusHistory
from apps.incidents.models import IncidentAudit
from apps.resorts.models import Resort


class DeviceViewSet(ViewSet):
    def create(self, request):
        user_id = request.data.get('user_id')

        if user_id is not None:
            user = get_user_model().objects.filter(user_id=user_id).first()
            if user is not None:
                if not user.is_active:
                    return Response({_("detail"): _("User inactive or deleted.")}, status=403)
                device_data = request.data

                try:
                    if not request.data.get('device_type', '').strip() or not request.data.get('device_type',
                                                                                               '').strip():
                        return Response({_('detail'): _('device type and/or device os can not be empty')}, status=400)
                except:
                    return Response({_('detail'): _('invalid data provided for device type and/or device os')},
                                    status=400)

                device_data = DeviceSerializer(data=device_data,
                                               fields=('device_type', 'device_os', 'device_push_token'))
                if device_data.is_valid():
                    device = device_data.save(device_user=user)
                    return Response({'device_id': device.device_id}, status=200)
                else:
                    return Response(device_data.errors, status=400)
            else:
                return Response({_("detail"): _("User does not exists")}, status=400)
        else:
            return Response({_("detail"): _("user_id is not provided")}, status=400)

    def update(self, request, pk=None):
        device = Devices.objects.filter(device_id=pk, device_state=0).first()
        response_data = {}

        if not request.user.is_active:
            return Response({_("detail"): _("User inactive or deleted.")}, status=403)

        if device is not None:
            device_data = DeviceSerializer(device, data=request.data, partial=True)
            if device_data.is_valid():
                device = device_data.save()
                device_data = DeviceSerializer(device,
                                               fields=('device_id', 'device_push_token', 'device_os', 'device_type',
                                                       'device_state', 'device_heartbeat_date'))
                response_data = device_data.data
                response_data['user_id'] = device.device_user.user_id
                return Response(response_data, status=200)
            else:
                return Response(device_data.errors, status=400)
        else:
            return Response({_("detail"): _("Device does not exists")}, status=400)

    def retrieve(self, request, pk=None):
        if not uuid(pk):
            return Response({_('detail'): _('not a valid UUID')}, status=400)

        device = Devices.objects.filter(device_id=pk, device_state=0).first()
        response_data = {}

        if not request.user.is_active:
            return Response({_("detail"): _("User inactive or deleted.")}, status=403)

        if device is not None:
            device_data = DeviceSerializer(device, fields=('device_id', 'device_push_token', 'device_os', 'device_type',
                                                           'device_state', 'device_heartbeat_date'))
            response_data = device_data.data
            response_data['user_id'] = device.device_user.user_id
            return Response(response_data, status=200)
        else:
            return Response({_("detail"): _("Device does not exists")}, status=400)

    @detail_route()
    def remotewipe(self, request, pk=None):

        device = Devices.objects.filter(device_id=pk, device_state=0).first()
        user = request.user

        if not request.user.is_active:
            return Response({_("detail"): _("User inactive or deleted.")}, status=403)

        if device is not None:
            if (device.device_state == 2) and (device.device_user == user):
                device.device_state = 1
                device.save()
                return Response({_("device_status"): _("deleted")}, status=200)
            else:
                return Response(
                    {_("detail"): _("either this device is not for deletion or does not belong to current user")},
                    status=403)
        else:
            return Response({_("detail"): _("Device does not exists")}, status=400)


@api_view(['GET'])
@permission_classes((AllowAny,))
@authentication_classes((OauthAuthentication, TokenAuthentication, SessionAuthentication))
def heartbeat(request, device_id=None):
    user = request.user
    include_status = map(int, request.query_params.get('include_status', '1, 2, 3, 4, 5, 6, 7').split(','))
    exclude_status = map(int, request.query_params.get('exclude_status', '8, 9').split(','))
    user_id = request.GET.get('user_id')

    if user_id is not None:
        try:
            user = get_user_model().objects.get(user_id=user_id)
        except ObjectDoesNotExist:
            return Response({_("detail"): _("User does not exists")}, status=400)

    if device_id is not None:
        try:
            # TODO Add "device_user=user" in the following query once functionality for many-to-many relation is in place.
            device = Devices.objects.get(device_id=device_id, device_state=0)
        except ObjectDoesNotExist:
            return Response({_("detail"): _("Device does not exists")}, status=400)
    else:
        return Response({_('detail'): _('device_id is not provided')}, status=400)

    resort_id = request.GET.get('resort_id')

    if resort_id is not None:
        try:
            resort = Resort.objects.get(resort_id=resort_id)
        except ObjectDoesNotExist:
            return Response({_("detail"): _("Resort does not exists")}, status=400)
    else:
        return Response({_('detail'): _('resort_id is not provided')}, status=400)

    # TODO Temporary removed the check. Enable once functionality for many-to-many relation is in place.
    # if device.device_user != user:
    #     return Response({_("detail"): _("Device does not belong to this user")}, status=403)

    try:
        user_heartbeat = Heartbeat.objects.get(user=user, device=device)
    except ObjectDoesNotExist:
        user_heartbeat = Heartbeat(user=user, device=device)
        user_heartbeat.save()

    response_data = {}
    function = {}

    # If device is pending deletion stage then send the remotewipe True else false
    if device.device_state == 2:
        function['remotewipe'] = True
    else:
        function['remotewipe'] = False

    if user_heartbeat.heartbeat_datetime is not None:
        if resort.dt_modified > user_heartbeat.heartbeat_datetime:
            function['getconfig'] = True
        else:
            function['getconfig'] = False
    else:
        function['getconfig'] = True

    if user_heartbeat.heartbeat_datetime is not None:
        get_incidents = Incident.objects.filter(assigned_to=user).filter(dt_modified__gte=user_heartbeat.heartbeat_datetime, incident_status__order__in=include_status).values_list('incident_id', flat=True)
    else:
        get_incidents = Incident.objects.filter(assigned_to=user).filter(incident_status__order__in=include_status).values_list('incident_id', flat=True)

    get_incidents_id = []
    for incident in get_incidents:
        get_incidents_id.append(str(incident))
    function['getincident'] = get_incidents_id

    delete_incident_id = []
    if user_heartbeat.heartbeat_datetime is not None:
        incident_audit = IncidentAudit.objects.filter(dt_created__gte=user_heartbeat.heartbeat_datetime, resort=resort)\
            .filter(prev_assigned_to=user).exclude(assigned_to=user) \
            .values_list('incident__incident_id', flat=True).distinct()

        incident_status_delete_list = StatusHistory.objects.filter(status__order__in=exclude_status,
                                                                   status_date__gte=user_heartbeat.heartbeat_datetime,
                                                                   incident__resort__resort_id=str(resort.resort_id))\
            .values_list('incident__incident_id', flat=True).distinct()
        common_list = list(set(incident_audit) | set(incident_status_delete_list))

        for incident in common_list:
            if not (str(incident) in get_incidents_id):
                delete_incident_id.append(str(incident))

    function['deleteincident'] = delete_incident_id

    language_file = Language.objects.latest('dt_created')

    response_data['msg'] = 'ok'
    response_data['function'] = function
    response_data['language_version'] = language_file.id

    user_heartbeat.heartbeat_datetime = timezone.now()
    user_heartbeat.save()

    return Response(response_data, status=200)
