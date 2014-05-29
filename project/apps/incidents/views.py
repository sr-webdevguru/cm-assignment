import base64
import logging
import os
import uuid as uid
from datetime import datetime
from datetime import timedelta

import pytz
import urllib
import urllib2
import os.path
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from apps.resorts.serializers import ResortSerializer
from django.db import transaction
from django.http.response import JsonResponse
from django.template import Context, Template
from django.template.context import RequestContext
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import ugettext as _
from pytz.exceptions import UnknownTimeZoneError
from rest_framework import viewsets, mixins, generics
from rest_framework.decorators import api_view, detail_route, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from sendfile import sendfile
from validators.uuid import uuid

from apps.authentication.custom_authentication_drf import OauthAuthentication
from apps.authentication.custom_authentication_drf import SessionAuthentication
from apps.authentication.custom_authentication_drf import TokenAuthentication
from apps.authentication.models import ResortOauthApp
from apps.custom_user.models import UserRoles
from apps.custom_user.utils import get_roleid_user
from apps.incidents.models import IncidentNotes
from apps.incidents.models import IncidentStatus, Incident
from apps.incidents.models import Patients
from apps.incidents.models import StatusHistory
from apps.incidents.serializers import IncidentNotesSerializer, IncidentListSerializer
from apps.incidents.serializers import IncidentStatusSerializer
from apps.incidents.serializers import StatusHistorySerializer
from apps.incidents.utils import audit_incident, incident_note, status_history, get_data_key
from apps.incidents.utils import check_drug_administered
from apps.incidents.utils import get_incident_data
from apps.incidents.utils import get_incident_sequence
from apps.incidents.utils import get_patient_info
from apps.incidents.utils import clean_data
from apps.incidents.utils import merge_incident
from apps.incidents.utils import merge_incident_data
from apps.incidents.utils import update_incident_data
from apps.incidents.utils import update_patient
from apps.incidents.utils import validate_incident_data
from apps.resorts.models import Resort
from apps.resorts.models import UserResortMap
from apps.resorts.utils import get_resort_for_user
from helper_functions import update_reference, create_s3_client
from oauth2_provider.models import AccessToken

note_field_mapping = {
    "field_52ca448dg94ja3": "note",
    "field_52ca448dg94ja4": "note_date",
    "field_52ca448dg94ja5": "user"
}

paper_mapping = {
    0: 'A4',
    1: 'Letter'
}

logger = logging.getLogger(__name__)


class Config(APIView):
    def get(self, request):
        resort_id = request.GET.get('resort_id')
        if resort_id is None or resort_id == '':
            return Response({_('detail'): _('resort_id not provided')}, status=400)

        if not uuid(resort_id):
            return Response({_('detail'): _('not a valid UUID')}, status=400)

        resort = Resort.objects.filter(resort_id=resort_id).first()

        if resort is not None:
            incident_template = resort.incident_template
        else:
            return Response({_('detail'): _('Resort does not exists')}, status=400)

        if request.user.user_connected == 0:
            incident_template['DashboardItems'].pop('field_52d47aac9bd13', None)
        else:
            try:
                patroller_sorted_list = sorted(
                    incident_template['DashboardItems']['field_52d47aac9bd13']['RepeatingQuestions']['patroller'][
                        'Values'], key=lambda k: k[k.keys()[0]].lower())
                incident_template['DashboardItems']['field_52d47aac9bd13']['RepeatingQuestions']['patroller'][
                    'Values'] = patroller_sorted_list
            except:
                pass

        if resort is not None:
            return Response(incident_template, status=200)
        else:
            return Response({_('detail'): _('Resort does not exists')}, status=400)

    def patch(self, request):
        resort_id = request.GET.get('resort_id')
        json = request.data

        if resort_id is None or resort_id == '':
            return Response({_('detail'): _('resort id not provided')})

        if not uuid(resort_id):
            return Response({_('detail'): _('not a valid UUID')})

        resort = Resort.objects.filter(resort_id=resort_id).first()

        if resort is not None:

            incident_template = dict(resort.incident_template.items() + json.items())
            resort.incident_template = incident_template
            resort.save()
        else:
            return Response({_('detail'): _('Resort does not exists')}, status=400)


class IncidentViewSet(viewsets.ViewSet, mixins.ListModelMixin, generics.GenericAPIView):
    def create(self, request):
        incoming_data = request.data
        incoming_data.pop('dateTimeFormat', None)
        user = request.user
        resort = get_resort_for_user(user)
        incoming_data, validation_error, missing_fields_with_data = validate_incident_data(incoming_data, resort)

        if validation_error:
            return Response(validation_error, status=400)

        logger.info("Create Incident",
                    extra={'request': request, 'tags': {'user': user.email}, 'data': {"data": request.data}})

        status = IncidentStatus.objects.get(pk=1)

        if resort.use_sequential_incident_id == 1 and user.user_connected == 1:
            incident_sequence = get_incident_sequence(resort)
        else:
            incident_sequence = 0

        try:
            new_incident = Incident(resort=resort, assigned_to=user, incident_status=status,
                                    incident_sequence=incident_sequence)
            new_incident.save()
            data_key = get_data_key(resort)
            incident_json = update_patient(incoming_data, new_incident.incident_pk, True, data_key)
        except:
            return Response({_('detail'): _('invalid incident information provided')}, status=400)

        notes = incident_note(incident_json, user, new_incident)
        if notes:
            new_incident.incident_json['notes'] = notes
            new_incident.save()

        audit_incident(new_incident, resort, user, user, user, incident_json)

        status_history(new_incident, status, user)

        return Response({"incident_id": new_incident.incident_id,
                         "incident_pk": new_incident.incident_sequence if resort.use_sequential_incident_id == 1 else new_incident.incident_pk},
                        status=200)

    def update(self, request, pk=None):
        incoming_data = request.data
        incoming_data.pop('dateTimeFormat', None)
        user = request.user
        resort = get_resort_for_user(user)
        incoming_data, validation_error, missing_fields_with_data = validate_incident_data(incoming_data, resort)

        if validation_error:
            logger.error("validation error",
                         extra={'request': request, 'detail': validation_error, 'tags': {'user': user.email},
                                'data': {"data": request.data}, "missing field": missing_fields_with_data})
            return Response(validation_error, status=400)

        logger.info("Update Incident",
                    extra={'request': request, 'tags': {'user': user.email}, 'data': {"data": request.data}})

        with transaction.atomic():
            incident = Incident.objects.select_for_update().filter(incident_id=pk).first()
            incoming_data = check_drug_administered(incoming_data, incident, user)
            data = incoming_data
            current_assigned = incident.assigned_to

            assigned_to = request.data.get('assigned_to')

            # Remove the redundant data from incident json
            data.pop('assigned_to', None)
            data.pop('incident_status', None)
            data.pop('incident_id', None)
            data.pop('incident_pk', None)
            data.pop('dateTimeFormat', None)

            assigned_user = None
            user_role = get_roleid_user(resort, user)

            # If incident status is deleted then dont allow the update of incident
            if incident.incident_status.order == 9:
                incident = None

            if incident is not None:
                # If user is patroller, then he/she can only update incident if following conditions are met
                # If incident is assigned to patroller
                # If incident is not in closed status
                if user_role == 1:
                    if incident.assigned_to != user or incident.incident_status.order == 8:
                        return Response({_("detail"): _("You do not have permission to edit this incident")},
                                        status=403)

                # If user is SOLO and incident is not assigned to him then deny the permission
                if user.user_connected == 0:
                    if incident.assigned_to != user:
                        return Response({_("detail"): _("You do not have permission to edit this incident")},
                                        status=403)

                if assigned_to is not None:
                    # Patroller does not have the permission to assign incident
                    assigned_user = get_user_model().objects.filter(user_id=assigned_to).first()
                    if assigned_user is None:
                        return Response({_("detail"): _("assigned_user does not exist")}, status=400)
                    if user_role == 1 and (not incident.assigned_to == assigned_user):
                        return Response({_("detail"): _("You do not have permission to assign this incident")},
                                        status=403)

                    incident.assigned_to = assigned_user
                else:
                    assigned_user = incident.assigned_to

                notes = incident_note(data, user, incident)
                if notes:
                    data['notes'] = notes

                # If incoming data contains dt_crated then update the it for incident
                if data.get('dt_created', ''):
                    dt_created = datetime.strptime(data.get('dt_created'), "%Y-%m-%d %H:%M:%S")
                    # if dt_created > (datetime.now() + timedelta(seconds=10)):
                    #     return Response({_("detail"): _("dt_created can not be a future date")}, status=400)
                    incident.dt_created = dt_created
                    data.pop('dt_created', None)

                incident_data = get_incident_data(incident.incident_pk)
                incident_data = clean_data(incident.resort, incident_data)
                data = merge_incident_data(incident_data, data)

                patient = Patients.objects.filter(incident=incident)

                data_key = get_data_key(resort)
                if patient:
                    # If incoming data has incident data then extract the patient data from it and also update the incident json
                    data = update_patient(data, incident.incident_pk, False, data_key)
                else:
                    data = update_patient(data, incident.incident_pk, True, data_key)

                incident.save()
                audit_incident(incident, resort, assigned_user, current_assigned, user, data)

                return Response({"incident_id": incident.incident_id}, status=200)
            else:
                return Response({_("detail"): _("Incident does not exist")}, status=400)


    def retrieve(self, request, pk=None):
        user = request.user
        incident = Incident.objects.filter(incident_id=pk).first()

        # If incident status is deleted then allow incident to be fetched
        if incident.incident_status.order == 9:
            incident = None

        if incident is not None:
            user_role = get_roleid_user(incident.resort, user)
            if user_role == 1 or user.user_connected == 0:
                if incident.assigned_to != user:
                    return Response({_("detail"): _("You do not have permission to retrieve the incident")}, status=403)

            response_data = get_incident_data(incident.incident_pk)
            response_data = clean_data(incident.resort, response_data)
            response_data['incident_id'] = str(incident.incident_id)
            if incident.resort.use_sequential_incident_id == 1:
                response_data['incident_pk'] = incident.incident_sequence
            else:
                response_data['incident_pk'] = incident.incident_pk

            response_data['assigned_to'] = str(incident.assigned_to.user_id)
            incident_status_data = IncidentStatusSerializer(incident.incident_status)
            response_data['incident_status'] = incident_status_data.data
            response_data['dt_created'] = datetime.strftime(incident.dt_created, "%Y-%m-%d %H:%M:%S")

            notes = IncidentNotes.objects.filter(incident=incident).order_by('-note_date')

            response_data['notes'] = IncidentNotesSerializer(notes, fields=('note_id', 'note_date', 'note', 'user'),
                                                             many=True).data
            data_key = get_data_key(incident.resort)
            response_data.update(get_patient_info(incident.incident_pk, data_key))
            return Response(response_data, status=200)
        else:
            return Response({_("detail"): _("Incident does not exist")}, status=400)

    def list(self, request, *args, **kwargs):
        user = self.request.user
        resort_id = request.query_params.get('resort_id')
        assigned_to = request.query_params.get('assigned_to')
        order_by = request.query_params.get('order_by', 'incident_pk')
        order_by_direction = request.query_params.get('order_by_direction', 'desc')
        include_status = map(int, request.query_params.get('include_status', '1, 2, 3, 4, 5, 6, 7, 8').split(','))

        if order_by_direction == 'desc':
            order = '-' + order_by
        elif order_by_direction == 'asc':
            order = order_by

        if resort_id is None:
            if not user.is_admin:
                resort = get_resort_for_user(user)
            else:
                resort = None
        else:
            if not uuid(resort_id):
                return Response({_('detail'): _('not a valid UUID')}, status=400)
            try:
                resort = Resort.objects.get(resort_id=resort_id)
            except ObjectDoesNotExist:
                return Response({_("detail"): _("Resort does not exists")}, status=400)

        user_role = get_roleid_user(resort, user)

        dateFrom = request.query_params.get('date_from', None)
        if dateFrom is None:
            dateFrom = datetime.today()
            dateFrom = dateFrom.strftime("%Y-%m-%d 00:00:00")
        else:
            dateFrom = (datetime.strptime(dateFrom, "%Y-%m-%d %H:%M:%S"))

        dateTo = request.query_params.get('date_to', None)
        if dateTo is None:
            dateTo = datetime.today()
            dateTo = dateTo.strftime("%Y-%m-%d 23:59:59")
        else:
            dateTo = (datetime.strptime(dateTo, "%Y-%m-%d %H:%M:%S"))

        # if request.query_params.get('date_from') is not None:
        #     date_from = datetime.datetime.strptime(request.query_params.get('date_from'), "%Y-%m-%d %H:%M:%S")
        # else:
        #     date_from = datetime.datetime.combine(timezone.now().date(), datetime.time(12, 0, 0))
        #
        # if request.query_params.get('date_to') is not None:
        #     date_to = datetime.datetime.strptime(request.query_params.get('date_to'), "%Y-%m-%d %H:%M:%S")
        # else:
        #     date_to = datetime.datetime.combine(timezone.now().date() + datetime.timedelta(days=1), datetime.time(12, 0, 0))

        if request.query_params.get('assigned_to') is not None:
            try:
                assigned_to = get_user_model().objects.get(user_id=request.query_params.get('assigned_to'))
            except ObjectDoesNotExist:
                return Response({_("detail"): _("assigned_to user does not exists")}, status=400)

        # If user is admin then show all the incidents across all the resorts
        if user.is_admin:
            if resort is None:
                query = Incident.objects.filter(dt_created__gte=dateFrom, dt_created__lte=dateTo,
                                                incident_status__order__in=include_status).order_by(order)
            else:
                query = Incident.objects.filter(resort=resort, dt_created__gte=dateFrom, dt_created__lte=dateTo,
                                                incident_status__order__in=include_status).order_by(order)

        # If user is resort patroller (or) connected to resort as SOLO user then only return incidents assigned to him
        elif user_role == 1 or user.user_connected == 0:
            query = Incident.objects.filter(resort=resort, assigned_to=user, dt_created__gte=dateFrom,
                                            dt_created__lte=dateTo, incident_status__order__in=include_status).order_by(
                order)

        # For manager, dispatcher connected with resort as networked user show all the incidents if assigned_to is not provided
        else:
            if assigned_to is None:
                query = Incident.objects.filter(resort=resort, dt_created__gte=dateFrom, dt_created__lte=dateTo,
                                                assigned_to__user_connected=1,
                                                incident_status__order__in=include_status).order_by(order)
            else:
                query = Incident.objects.filter(resort=resort, assigned_to=assigned_to, dt_created__gte=dateFrom,
                                                dt_created__lte=dateTo,
                                                incident_status__order__in=include_status).order_by(order)

        queryset = self.filter_queryset(query)

        page = self.paginate_queryset(queryset)
        if page is not None:
            data_key = get_data_key(resort)
            serializer = IncidentListSerializer(page, fields=(
            'incident_pk', 'incident_id', 'dt_created', 'resort', 'incident_status', 'assigned_to'),
                                            many=True, context={'data_key': data_key})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def media(self, request, pk=None):
        user = request.user
        resort = get_resort_for_user(user)
        updated = False

        data = request.data.copy()
        data.pop('media')

        try:
            incident = Incident.objects.get(incident_id=pk)
            if incident.incident_status.order == 9:
                raise ObjectDoesNotExist
        except ObjectDoesNotExist:
            logger.info("Media API Log",
                        extra={'request': request, 'tags': {'user': user.email}, 'data': {"data": data},
                               "reason": "Incident does not exists"})
            return Response({_("detail"): _('Incident does not exists')}, status=400)

        if incident.resort != resort:
            logger.info("Media API Log",
                        extra={'request': request, 'tags': {'user': user.email}, 'data': {"data": data},
                               "reason": "You do not have permission to add media to this incident"})
            return Response({_("detail"): _('You do not have permission to add media to this incident')}, status=403)

        mime_type = request.data.get('mimeType')

        if (mime_type is None) or (not mime_type):
            logger.info("Media API Log",
                        extra={'request': request, 'tags': {'user': user.email}, 'data': {"data": data},
                               "reason": "mimeType is required"})
            return Response({_("detail"): _('mimeType is required')}, status=400)

        try:
            fileformat = mime_type.split('/')[1]
        except:
            logger.info("Media API Log",
                        extra={'request': request, 'tags': {'user': user.email}, 'data': {"data": data},
                               "reason": "invalid mime_type provide"})
            return Response({_('detail'): _('invalid mime_type provided')}, status=400)

        file_name = str(uid.uuid4()) + '.' + fileformat

        media_content = request.data.get('media')

        if (media_content is None) or (not media_content):
            logger.info("Media API Log",
                        extra={'request': request, 'tags': {'user': user.email}, 'data': {"data": data},
                               "reason": "media content not provided"})
            return Response({_('detail'): _('media content not provided')}, status=400)

        try:
            # Create new s3 client
            client = create_s3_client()
            media_file = base64.decodestring(media_content)

            # Use global KMS Key for Encryption
            kms_key = settings.GLOBAL_KMS_KEY_ID

            # If resort has its own CMK then use it instead of global one
            if resort.kms_enabled and resort.kms_cmk != "" and (resort.kms_cmk is not None):
                kms_key = resort.kms_cmk

            response = client.put_object(Body=media_file, Bucket=settings.BUCKET_NAME, Key="%s/%s/%s" % (str(resort.resort_id), str(incident.incident_id), file_name), ServerSideEncryption="aws:kms", SSEKMSKeyId=kms_key)
        except:
            logger.info("Media API Log",
                        extra={'request': request, 'tags': {'user': user.email}, 'data': {"data": data},
                               "reason": "base64 string is not valid"})
            return Response({_('detail'): _('base64 string is not valid')}, status=400)

        media_path = settings.SCHEME + request.get_host() + '/content/' + str(resort.resort_id) + '/' + str(
            incident.incident_id) + '/' + file_name

        # Checks for media reference in the request
        media_reference = request.data.get('media_reference', '')

        # If we found media reference then proceed with replacing media reference with URL in incident json
        if media_reference:
            incident_json = get_incident_data(incident.incident_pk)
            incident_json, updated = update_reference(incident_json, media_reference, media_path)

            if updated != 1:
                logger.info("Media API Log",
                            extra={'request': request, 'tags': {'user': user.email}, 'data': {"data": data},
                                   "reason": "media_reference not found in incident",
                                   "incident": {"incident data": incident_json}})
                return Response({_('detail'): _('media_reference not found in incident')}, status=400)

            update_incident_data(incident.incident_pk, incident_json)

        logger.info("Media API Log", extra={'request': request, 'tags': {'user': user.email}, 'data': {"data": data},
                                            "reason": "all ok"})
        return Response({_('media_url'): media_path, 'mimeType': mime_type, 'media_reference': media_reference},
                        status=200)

    @detail_route()
    def patient(self, request, pk=None):

        try:
            incident = Incident.objects.get(incident_id=pk)
            if incident.incident_status.order == 9:
                raise Exception
        except:
            return Response({_('detail'): _('incident does not exists')}, status=400)

        data_key = get_data_key(incident.resort)
        return Response(get_patient_info(incident.incident_pk, data_key), status=200)

    @detail_route(url_path='print')
    def print_incident(self, request, pk=None):

        response = IncidentViewSet().retrieve(request, pk)
        incident_data = response.data

        try:
            incident = Incident.objects.get(incident_id=pk)
            if incident.incident_status.order == 9:
                raise Exception
        except:
            return Response({_('detail'): _('incident does not exists')}, status=400)

        data = {}
        data['DashboardItems'] = merge_incident(incident_data, incident.resort)
        data['incident_info'] = incident_data
        data['status_history'] = StatusHistorySerializer(
            StatusHistory.objects.filter(incident=incident).order_by('status_date'), many=True).data
        data['incident'] = incident
        paper_size = paper_mapping[incident.resort.default_unit_paper]

        try:
            data['timez'] = pytz.timezone(incident.resort.timezone)
        except UnknownTimeZoneError:
            return Response({_('detail'): _('Please set the correct timezone for resort')}, status=400)

        pdf_name = str(incident.incident_id) + '_' + paper_size + '.pdf'

        dir_path = os.path.join(settings.SENDFILE_ROOT)
        incident_media_path = os.path.join(dir_path, 'media', pdf_name)
        media_path = settings.SENDFILE_ROOT
        incident_pdf_path = os.path.join(media_path, pdf_name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        if not os.path.exists(media_path):
            os.makedirs(media_path)

        if not os.path.exists(os.path.join(dir_path, 'media')):
            os.makedirs(os.path.join(dir_path, 'media'))


        resort = ResortSerializer(incident.resort, fields=('resort_id', 'resort_name', 'map_kml',
                                                           'map_type', 'location', 'print_on_device',
                                                           'map_lat', 'map_lng', 'network_key',
                                                           'license_expiry_date', 'licenses',
                                                           'report_form', 'website', 'domain_id',
                                                           'unit_format', 'timezone', 'resort_logo',
                                                           'dispatch_field_choice', 'datetime_format',
                                                           'resort_controlled_substances', 'resort_asset_management'))

        tmpFile = urllib.urlretrieve(resort.data["report_form"])
        contents = open(tmpFile[0]).read()
        fileName = resort.data["report_form"].split('/')[-1]
        filepath= os.path.abspath(settings.TEMPLATE_DIRS[0]) + '/' + fileName
        f = open(filepath, 'w')
        f.write(contents)
        f.close()
        # If file does not exists then create new one and add it to the response
        rendered_html = render_to_string(template_name=fileName,
                                         dictionary=data, context_instance=RequestContext(request))
        # Write rendered string to the file
        file_name = str(uid.uuid4()) + '.html'
        file_path =  incident_pdf_path + '.html'
        with open(file_path, 'w+') as html_file:
            html_file.write(rendered_html.encode('utf-8'))
            html_file.close()
        # call wkhtmltopdf from commandline to print pdf
        if settings.RUN_ENV == 'local':
            os.system('wkhtmltopdf -s %s -O landscape %s %s' % (paper_size, file_name, incident_pdf_path))
        else:
            os.system(os.path.join(settings.BASE_DIR, 'medic52/wkhtmltopdf-amd64') + ' -s %s -O portrait %s %s' % ( paper_size, file_path, incident_media_path))
        # Remove temporary file
        os.remove(file_path)
        # Send the generated file
        return sendfile(request, incident_media_path, attachment=True)


@api_view(['GET'])
def get_status_list(request):
    status_list = IncidentStatus.objects.all().order_by('order')

    status_data = IncidentStatusSerializer(status_list, many=True)
    return Response(status_data.data, status=200)


class IncidentStatusView(APIView):
    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            incident_id = kwargs.get('uuid')

            if not uuid(incident_id):
                return Response({_('detail'): _('not a valid UUID')}, status=400)

            try:
                incident = Incident.objects.select_for_update().get(incident_id=incident_id)
                if incident.incident_status.order == 9:
                    raise ObjectDoesNotExist
            except ObjectDoesNotExist:
                return Response({_("detail"): _("Incident does not exists")}, status=400)

            user_role = get_roleid_user(incident.resort, request.user)
            status_id = int(request.data.get('status_type_id'))

            if user_role != 3 and incident.incident_status.order == 8:
                return Response({_("detail"): _("You do not have permission to open this incident")}, status=403)
            elif user_role == 1 and status_id == 9:
                return Response({_("detail"): _("You do not have permission to delete this incident")}, status=403)

            if status_id is not None:
                try:
                    status = IncidentStatus.objects.get(incident_status_id=status_id)
                except ObjectDoesNotExist:
                    return Response({_("detail"): _("incident status not found")}, status=400)

            updated_by = request.data.get('updated_by')

            if updated_by is not None:
                try:
                    updated_user = get_user_model().objects.get(user_id=updated_by)
                except ObjectDoesNotExist:
                    return Response({_("detail"): _("updated_by user not found")}, status=400)
            else:
                updated_user = request.user

            incident.incident_status = status
            incident.save()

            if request.data.get('status_date') is not None:
                timestamp = datetime.strptime(request.data.get('status_date'), "%Y-%m-%d %H:%M:%S")
            else:
                timestamp = timezone.now()

            status_history(incident, status, updated_user, timestamp)

            return Response({"incident_id": incident.incident_id}, status=200)

    def get(self, request, *args, **kwargs):
        incident_id = kwargs.get('uuid')
        response_data = {}
        status_data = []

        if not uuid(incident_id):
            return Response({_('detail'): _('not a valid UUID')}, status=400)

        try:
            incident = Incident.objects.get(incident_id=incident_id)
            if incident.incident_status.order == 9:
                raise ObjectDoesNotExist
        except ObjectDoesNotExist:
            return Response({_("detail"): _("Incident does not exists")}, status=400)

        status_history = StatusHistory.objects.filter(incident=incident).order_by('status_date')

        for status in status_history:
            status_data.append(StatusHistorySerializer(status, fields=('status_history_id', 'status', 'status_date',
                                                                       'user')).data)

        response_data['status_count'] = len(status_history)
        response_data['status'] = status_data

        return Response(response_data, status=200)


class IncidentNotesView(APIView):
    def post(self, request, *args, **kwargs):
        incident_id = kwargs.get('uuid')

        if not uuid(incident_id):
            return Response({_('detail'): _('not a valid UUID')}, status=400)

        try:
            incident = Incident.objects.get(incident_id=incident_id)
            if incident.incident_status.order == 9:
                raise Exception
        except ObjectDoesNotExist:
            return Response({_("detail"): _("Incident does not exists")}, status=400)

        if request.data.get('field_52ca448dg94ja4') is not None:
            timestamp = datetime.strptime(request.data.get('field_52ca448dg94ja4'), "%Y-%m-%d %H:%M:%S")
        else:
            timestamp = datetime.now()

        note = IncidentNotes(incident=incident, note=request.data.get('field_52ca448dg94ja3'), note_date=timestamp,
                             user=request.user)
        note.save()

        note_response = IncidentNotesSerializer(note, fields=('note_id', 'note_date', 'note'))

        return Response(note_response.data, status=200)

    def get(self, request, *args, **kwargs):
        incident_id = kwargs.get('uuid')
        response_data = {}

        if not uuid(incident_id):
            return Response({_('detail'): _('not a valid UUID')}, status=400)

        try:
            incident = Incident.objects.get(incident_id=incident_id)
            if incident.incident_status.order == 9:
                raise Exception
        except ObjectDoesNotExist:
            return Response({_("detail"): _("Incident does not exists")}, status=400)

        notes = IncidentNotes.objects.filter(incident_id=incident).order_by('-note_date')

        notes = IncidentNotesSerializer(notes, fields=('note_id', 'note_date', 'note', 'user'), many=True)

        response_data['results'] = notes.data
        response_data['count'] = len(notes.data)
        response_data['incident_id'] = incident_id

        return Response(response_data, status=200)


@api_view()
@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication, SessionAuthentication))
def media_access(request, resort_id=None, incident_id=None):
    # get the authenticated user from request
    user = request.user

    '''
    Try authenticating the identity of user
    # Get resort - To check if resort_id is correct (or) not
    # Get incident - To check if incident_id is correct (or) not
    # Get User_Resort_Map - To check if user has access to particular resort (or) not
    # If any of the above generated exception then file not found reply is sent back
    '''
    try:
        resort = Resort.objects.get(resort_id=resort_id)
        incident = Incident.objects.get(incident_id=incident_id)
        user_resort = UserResortMap.objects.get(user=user, resort=resort)
        if incident.incident_status.order == 9:
            raise Exception
    except:
        return JsonResponse({_("detail"): _("file not found")}, status=404)

    '''
    If above criteria is matched then file path is set in the X-Accel-Redirect header by sendfile module.
    Nginx then uses the header to serve media to the user
    '''
    # Remove any old files from the temp directory
    safetime = datetime.now() - timedelta(minutes=5)

    # Path to temporary directory in media folder
    dir_path = os.path.join(settings.MEDIA_ROOT, 'media', 'tmp')

    # Remove the file which has been there for more than 5 min in the temp directory
    for each_file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, each_file)
        if os.path.isfile(file_path):
            file_modification_datetime = datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_modification_datetime < safetime:
                os.remove(file_path)

    # If temp does not exists then create new one
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # Extract the key for retrieving file from s3
    file_key = request.path.replace('/content/', '')

    # Create new s3 client
    client = create_s3_client()

    # Get the file from s3
    response = client.get_object(Bucket=settings.BUCKET_NAME, Key=file_key)

    # Write the file content to temporary file
    with open(os.path.join(dir_path, file_key.split('/')[2]), 'wb') as file_to_receive:
        file_to_receive.write(response['Body'].read())

    media_path = os.path.join(dir_path, file_key.split('/')[2])
    return sendfile(request, media_path)


@api_view(['POST'])
@permission_classes((AllowAny,))
@authentication_classes((OauthAuthentication,))
def public_incident(request):
    access_token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
    access_token_object = AccessToken.objects.get(token=access_token)
    resort = None

    try:
        resort_oauth_application = ResortOauthApp.objects.get(oauth_app=access_token_object.application)
        resort_network_key = request.data.get('resort_network_key')
        if resort_network_key is not None:
            resort = Resort.objects.get(network_key=resort_network_key)
            if resort != resort_oauth_application.resort:
                raise Exception
        else:
            return Response({_('detail'): _('resort_network_key is not provided')}, status=400)
    except:
        return Response({_('detail'): _('you do not have access to this resource')}, status=400)

    missing_field = []
    for key in ['reporter_name', 'reporter_phone', 'field_52ca456962ba8']:
        if not request.data.has_key(key):
            missing_field.append(key)
    if missing_field:
        return Response({_('detail'): "missing the field %s" % ','.join(missing_field)}, status=400)

    status = IncidentStatus.objects.get(pk=1)
    incoming_data = request.data
    incoming_data.pop('resort_network_key', None)
    incoming_data, validation_error, missing_fields_with_data = validate_incident_data(incoming_data, resort)

    if validation_error:
        return Response(validation_error, status=400)

    if resort.use_sequential_incident_id == 1:
        incident_sequence = get_incident_sequence(resort)
    else:
        incident_sequence = 0

    user_role = UserRoles.objects.get(role_id=2)
    assigned_user = UserResortMap.objects.filter(resort=resort, role=user_role, user__user_connected=1).first()

    try:
        new_incident = Incident(resort=resort, assigned_to=assigned_user.user, incident_status=status,
                                incident_sequence=incident_sequence)
        new_incident.save()
        data_key = get_data_key(resort)
        incident_json = update_patient(incoming_data, new_incident.incident_pk, True, data_key)
    except:
        return Response({_('detail'): _('invalid incident information provided')}, status=400)

    return Response({'incident_id': new_incident.incident_id}, status=200)


@api_view(['POST'])
@permission_classes((AllowAny,))
@authentication_classes((OauthAuthentication,))
def upload_file_to_s3(request):
    messages = []
    resorts = []
    not_found_id = []
    # Create s3 client with provided credential
    client = create_s3_client()

    # Media directory where all media files are located
    media_path = os.path.join(settings.MEDIA_ROOT, 'media')

    # Iterate through each of the media directory
    # First level describes resort_id
    for each_dir in os.listdir(media_path):
        if uuid(each_dir):
            try:
                # Fetch the resort to check KMS settings
                resort = Resort.objects.get(resort_id=each_dir)
                resorts.append(resort.resort_name)
            except ObjectDoesNotExist:
                not_found_id.append(each_dir)
                continue
            media_incident_path = os.path.join(media_path, each_dir)
            # Interate through second level which describes incident_id
            for each_incident_dir in os.listdir(media_incident_path):
                if uuid(each_incident_dir):
                    for each_file in os.listdir(os.path.join(media_incident_path, each_incident_dir)):
                        # Use global KMS Key for Encryption
                        kms_key = settings.GLOBAL_KMS_KEY_ID

                        # If resort has its own CMK then use it instead of global one
                        if resort.kms_enabled and resort.kms_cmk != "" and (resort.kms_cmk is not None):
                            kms_key = resort.kms_cmk
                        if os.path.isfile(os.path.join(media_incident_path, each_incident_dir, each_file)):
                            with open(os.path.join(media_incident_path, each_incident_dir, each_file)) as file_to_upload:
                                response = client.put_object(Body=file_to_upload.read(), Bucket=settings.BUCKET_NAME, Key="%s/%s/%s" % (each_dir, each_incident_dir, each_file), ServerSideEncryption="aws:kms", SSEKMSKeyId=kms_key)
                            messages.append(resort.resort_name + " File with Key " + "%s/%s/%s" % (each_dir, each_incident_dir, each_file) + " Uploaded Successfully")
    return Response({"messages": messages, "resorts found": resorts, "not found resort": not_found_id}, status=200)