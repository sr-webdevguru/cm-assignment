# -*- coding: utf-8 -*-
from collections import OrderedDict
from datetime import datetime, timedelta

import pytz
import cStringIO as StringIO
import csv
from django.conf import settings
from django.db import connection
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from pytz import timezone
from rest_framework import viewsets
from apps.custom_user.utils import get_roleid_user
from rest_framework.decorators import list_route
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from sendfile import sendfile

from apps.incidents.analytics import get_param
from apps.incidents.models import Incident, IncidentStatus
from apps.incidents.serializers import IncidentReportSerializer, IncidentStatusReportSerializer, \
    IncidentStatusSerializer
from apps.reports.utils import add_missing_data, incident_status_grouping, transform_injury_repeater
from apps.reports.utils import create_report
from apps.reports.utils import dict_to_csv_report
from apps.reports.utils import extract_date_chart
from apps.reports.utils import get_report
from apps.reports.utils import get_report_data_for_csv
from apps.reports.utils import incident_template_field_type_mapping
from apps.reports.utils import list_report
from apps.reports.utils import merge_compare_data
from apps.reports.utils import process_pie_chart_data
from apps.reports.utils import update_report
from apps.incidents.utils import dictfetchall, get_data_key
from apps.resorts.models import Resort
from apps.resorts.utils import get_resort_for_user

patient_fields = ["name", "sex", "address", "suburb", "state", "postcode", "country", "phone", "email", "dob"]
note_fields = ["notes____field_52ca448dg94ja3", "notes____field_52ca448dg94ja4", "notes____field_52ca448dg94ja5"]
location_field = ["field_52ca456962ba8____lat", "field_52ca456962ba8____long", "field_52ca456962ba8____accuracy"]
encrypted_fields = ["name", "address", "suburb", "state", "postcode", "phone", "email", "dob"]
note_field_map = {"notes____field_52ca448dg94ja3": "note", "notes____field_52ca448dg94ja4": "note_date",
                  "notes____field_52ca448dg94ja5": "user"}
scale_mapping = {'day': 'day', 'hour': 'hour', 'day_of_week': 'dow', 'week_of_year': 'week', 'month_of_year': 'month',
                 'year': 'year', 'date': 'date', 'hour_of_day_of_week': 'hdow'}
date_mapping = ['%m-%d-%Y','%d-%m-%Y']


def get_param_with_pagination(request):
    dateFrom, dateTo, resort = get_param(request)
    output_format = request.GET.get('output_format', 'json')
    order_by = request.query_params.get('order_by', 'name')
    order_by_direction = request.query_params.get('order_by_direction', 'asc')
    chunk = request.query_params.get('chunk', None)
    offset = request.query_params.get('offset', 0)
    if offset < 0: offset = 0
    if output_format.upper() != 'CSV': output_format = 'json'
    if chunk is not None: chunk = int(chunk)
    return dateFrom, dateTo, resort, chunk, int(offset), order_by, order_by_direction.upper(), output_format


def get_param_post(request):
    resort_id = request.query_params.get('resort_id', None)

    try:
        resort = Resort.objects.get(resort_id=resort_id)
    except:
        resort = get_resort_for_user(user=request.user)

    dateFrom = request.query_params.get('datefrom', None)
    if dateFrom is None or not dateFrom:
        dateFrom = datetime.today() - timedelta(days=7)
        dateFrom = dateFrom.strftime("%Y-%m-%d 00:00:00")
    else:
        dateFrom = (datetime.strptime(dateFrom, "%Y-%m-%d %H:%M:%S"))
        dateFrom = timezone('UTC').localize(dateFrom)
        dateFrom = dateFrom.astimezone(timezone(resort.timezone))

    dateTo = request.query_params.get('dateto', None)
    if dateTo is None or not dateTo:
        dateTo = datetime.today()
        dateTo = dateTo.strftime("%Y-%m-%d 23:59:59")
    else:
        dateTo = (datetime.strptime(dateTo, "%Y-%m-%d %H:%M:%S"))
        dateTo = timezone('UTC').localize(dateTo)
        dateTo = dateTo.astimezone(timezone(resort.timezone))

    return dateFrom, dateTo, resort


class ReportViewset(viewsets.ViewSet):
    def create(self, request):
        response = {}
        if request.user.user_connected == 0:
            return Response({_('detail'): _('you do not have permission to create report')}, status=403)

        resort = get_resort_for_user(request.user)

        response_data = create_report(request.data.get('global', 0), request.user, request.data, resort)
        response.update(response_data['report_config'])
        response.update({"report_id": response_data['report_id']})
        return Response(response)

    def update(self, request, pk=None):
        if request.user.user_connected == 0:
            return Response({_('detail'): _('you do not have permission to update report')}, status=403)

        response = {}
        response_data = update_report(request.data['global'], request.user, request.data, pk)

        response.update(response_data['report_config'])
        response.update({"report_id": response_data['report_id']})
        return Response(response)

    def list(self, request):
        response_data = {}
        if request.user.user_connected == 0:
            return Response({_('detail'): _('you do not have permission to list report')}, status=403)

        response_data['results'] = list_report(request.user)
        response_data['count'] = len(response_data['results'])
        return Response(response_data)

    def retrieve(self, request, pk=None):
        response_data = {}
        if request.user.user_connected == 0:
            return Response({_('detail'): _('you do not have permission to retrieve report')}, status=403)
        data = get_report(pk)
        response_data.update(data['report_config'])
        response_data.update({"report_id": data['report_id']})
        return Response(response_data)

    @list_route(methods=['get'])
    def patrollers(self, request):
        order_by_fields = ['name', 'primary', 'secondary', 'assist', 'total']

        dateFrom, dateTo, resort, chunk, offset, orderBy, orderByDirection, outputFormat = get_param_with_pagination(request)
        user_role = get_roleid_user(resort, request.user)
        original_data_len = 0

        if user_role == 1:
            return Response({_("detail"): _("You do not have permission to view analytics")}, status=403)

        if orderBy not in order_by_fields:
            orderBy = order_by_fields[0]
        with connection.cursor() as cursor:
            cursor.execute("""SELECT
  json_array_elements(CAST (resorts_resort.incident_template AS JSON)->'DashboardItems'->'field_52d47aac9bd13'->
  'RepeatingQuestions'->'patroller'->'Values') ->> (patrollers_incident->>'patroller') as name,
  SUM(CASE WHEN CAST (patrollers_incident->'incident_role' AS text) = '"170"' THEN 1 ELSE 0 END) AS "primary",
  SUM(CASE WHEN CAST (patrollers_incident->'incident_role' AS text) = '"171"' THEN 1 ELSE 0 END) AS "secondary",
  SUM(CASE WHEN CAST (patrollers_incident->'incident_role' AS text) = '"172"' THEN 1 ELSE 0 END) AS "assist",
  SUM(CASE WHEN CAST (patrollers_incident->'incident_role' AS text) = '"170"' THEN 1 ELSE 0 END +
  CASE WHEN CAST (patrollers_incident->'incident_role' AS text) = '"171"' THEN 1 ELSE 0 END +
  CASE WHEN CAST (patrollers_incident->'incident_role' AS text) = '"172"' THEN 1 ELSE 0 END) AS "total"
FROM
    incidents_incident INNER JOIN custom_user_users ON custom_user_users.user_pk = incidents_incident.assigned_to_id,
    json_array_elements(incidents_incident.incident_data->'field_52d47aac9bd13') as patrollers_incident
LEFT JOIN resorts_resort ON resorts_resort.resort_pk = %d
WHERE
    CAST (patrollers_incident AS text) <> '[]'
    AND CAST (patrollers_incident AS text) <> 'false'
    AND CAST (patrollers_incident AS text) <> ''
    AND incidents_incident.resort_id = %d
    AND custom_user_users.user_connected = %d
    AND incidents_incident.dt_created IS NOT NULL AND incidents_incident.dt_created >= '%s' AND incidents_incident.dt_created <= '%s'
    AND incidents_incident.incident_status_id <> 9
GROUP BY 1
ORDER BY %s %s;""" % (resort.resort_pk, resort.resort_pk, request.user.user_connected, dateFrom, dateTo, "\"" + orderBy
                      + "\"", orderByDirection))
            data = dictfetchall(cursor)
            print resort, request.user
            if data:
                # Delete the global group row.
                pop_index = 0 if orderByDirection == 'DESC' else (len(data) - 1)
                data.pop(pop_index)
                original_data_len = len(data)
                # Pagination
                if offset is not 0:
                    data = data[offset:]
                if chunk is not None:
                    chunk = chunk if chunk <= len(data) else len(data)
                    data = data[:chunk]

        if outputFormat.upper() == 'CSV':
            def toCSV(content):
                csvfile = StringIO.StringIO()
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(["name", "primary", "secondary", "assist", "total"])
                yield csvfile.getvalue()
                for row in content:
                    csvfile = StringIO.StringIO()
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow([row["name"], row["primary"], row["secondary"], row["assist"], row["total"]])
                    yield csvfile.getvalue()
            response = HttpResponse(toCSV(data), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="patrollers_report.csv"'
            return response
        else:
            return Response({
                'success': True,
                'data': data,
                'total_rows': original_data_len
            }, status=200)

    @list_route(methods=['post'])
    def table(self, request):

        if request.user.user_connected == 0:
            return Response({_('detail'): _('you do not have access to report')}, status=403)

        dateFrom, dateTo, resort = get_param_post(request)
        text_data_key = get_data_key(resort)

        chunk = int(request.query_params.get('chunk', 100))
        offset = int(request.query_params.get('offset', 0))
        output_format = request.query_params.get('output_format', 'json')
        from_query = ''
        where_query = ''
        inner_join = ''
        cross_join = ''
        table_no = 0
        inner_patient = False
        inner_note = False
        response_data = {}
        where_parameters = []

        b = incident_template_field_type_mapping(resort.incident_template)
        def shouldRegex(field):
            if field == 'field_539158b37814e': return False
            if field == 'field_52dd8a24e95a6': return False
            if field == 'field_53c386190a2dd': return False
            if field == 'field_5334b101c8779': return False
            if field == 'field_52ca437b62b9c': return False
            if field == 'field_52ca43f362ba0': return False
            if field == 'field_52ca429c62b98': return False
            if field == 'field_52ca405959d2c': return False
            if field == 'field_52ca3fcc59d29': return False
            if field == 'field_52ca431e62b9b': return False
            if field == 'field_54b084fb2d255': return False
            return True

        for data_key, data_value in request.data.iteritems():

            if data_key in patient_fields:
                if not inner_patient:
                    inner_join += ' INNER JOIN incidents_patients ON incidents_patients.incident_id = incidents_incident.incident_pk'
                    cross_join += """CROSS JOIN (SELECT '%s'::TEXT As datakey) As keys""" % (
                        text_data_key)
                    inner_patient = True
                data_length = len(data_value)

                if data_length == 1:
                    if data_key in encrypted_fields:
                        where_query += " AND pgp_sym_decrypt(incidents_patients.%s, keys.datakey) ILIKE %s" % (
                            data_key, '%s')
                        where_parameters.append("%" + data_value[0] + "%")
                    elif data_key == 'sex':
                        where_query += " AND incidents_patients.%s = %s" % ('sex', '%s')
                        where_parameters.append(data_value[0].lower())
                    else:
                        where_query += " AND incidents_patients.%s ILIKE %s" % (data_key, '%s')
                        where_parameters.append(data_value[0])
                else:
                    temp_query = ''
                    for id, value in enumerate(data_value):
                        if data_key in encrypted_fields:
                            temp_query += "%spgp_sym_decrypt(incidents_patients.%s, keys.datakey) ILIKE %s" % (
                                " OR " if id > 0 else "", data_key, '%s')
                            where_parameters.append("%" + data_value[id] + "%")
                        elif data_key == 'sex':
                            temp_query += "%sincidents_patients.%s = %s" % (" OR " if id > 0 else "", 'sex', '%s')
                            where_parameters.append(data_value[id].lower())
                        else:
                            temp_query += "%sincidents_patients.%s ILIKE %s" % (
                                " OR " if id > 0 else "", data_key, '%s')
                            where_parameters.append(data_value[id])
                    where_query += " AND " + "(" + temp_query + ")"

            elif data_key in note_fields:
                if not inner_note:
                    inner_join += ' INNER JOIN incidents_incidentnotes ON incidents_incidentnotes.incident_id = incidents_incident.incident_pk'
                    inner_note = True
                data_length = len(data_value)

                if data_length == 1:
                    where_query += " AND incidents_incidentnotes.%s ILIKE %s" % (
                        note_field_map[data_key], '%s')
                    where_parameters.append("%" + data_value[0] + "%")
                else:
                    temp_query = ""
                    for id, value in enumerate(data_value):
                        temp_query += "%sincidents_incidentnotes.%s ILIKE %s" % (
                            " OR " if id > 0 else "", note_field_map[data_key], '%s')
                        where_parameters.append("%" + data_value[id] + "%")
                    where_query += " AND " + "(" + temp_query + ")"

            elif data_key in location_field:
                if not 'field_52ca456962ba8' in from_query:
                    from_query += ", CAST((incidents_incident.incident_data -> 'field_52ca456962ba8') AS JSON) as location_json"
                data_length = len(data_value)

                if data_length == 1:
                    where_query += " AND (location_json ->> '%s') ILIKE %s" % (
                        data_key.split('____')[1], '%s')
                    where_parameters.append("%" + data_value[0] + "%")
                else:
                    temp_query = ""
                    for id, value in enumerate(data_value):
                        temp_query += "%s(location_json ->> '%s') ILIKE %s" % (
                            " OR " if id > 0 else "", data_key.split('____')[1], '%s')
                        where_parameters.append("%" + data_value[id] + "%")
                    where_query += " AND " + "(" + temp_query + ")"

            elif b[data_key]['type'] == 'text' or b[data_key]['type'] == 'int':
                data_length = len(data_value)

                if data_length == 1:
                    where_query += " AND (incident_data ->> '%s') %s %s" % (
                        b[data_key]['key'], "ILIKE" if type(data_value[0]) in [str, unicode] else "=", '%s')
                    if shouldRegex(data_key):
                        where_parameters.append(
                            "%" + data_value[0] + "%" if type(data_value[0]) in [str, unicode] else str(data_value[0]))
                    else:
                        where_parameters.append(data_value[0])
                else:
                    temp_query = ""
                    for id, value in enumerate(data_value):
                        temp_query += "%s(incident_data ->> '%s') %s %s" % (
                            " OR " if id > 0 else "", b[data_key]['key'],
                            "ILIKE" if type(data_value[0]) in [str, unicode] else "=",
                            '%s')
                        where_parameters.append(
                            "%" + data_value[id] + "%" if type(data_value[id]) in [str, unicode] else str(
                                data_value[id]))
                    where_query += " AND " + "(" + temp_query + ")"
            elif b[data_key]['type'] == 'array':
                if not b[data_key]['key'] in from_query:
                    from_query += ", json_array_elements(incidents_incident.incident_data -> '%s') as table%d" % (
                        b[data_key]['key'], table_no)
                data_length = len(data_value)

                if data_length == 1:
                    where_query += " AND CAST(table%d AS TEXT) = %s" % (table_no, '%s')
                    where_parameters.append('"' + data_value[0] + '"')
                else:
                    temp_query = ""
                    for id, value in enumerate(data_value):
                        temp_query += "%sCAST(table%d AS TEXT) = %s" % (" OR " if id > 0 else "", table_no, '%s')
                        where_parameters.append('"' + data_value[id] + '"')
                    where_query += " AND " + "(" + temp_query + ")"
                table_no += 1
            elif 'repeating' in b[data_key]['type']:
                if not b[data_key]['key'] in from_query:
                    from_query += ", CAST(json_array_elements(incidents_incident.incident_data -> '%s') AS JSON) as table%d" % (
                        b[data_key]['key'], table_no)

                data_length = len(data_value)

                if data_length == 1:
                    where_query += " AND (table%d ->> '%s') ILIKE %s" % (
                        table_no, b[data_key]['sub_key'], '%s')
                    where_parameters.append("%" + data_value[0] + "%")
                else:
                    temp_query = ""
                    for id, value in enumerate(data_value):
                        temp_query += "%s(table%d ->> '%s') ILIKE %s" % (
                            " OR " if id > 0 else "", table_no, b[data_key]['sub_key'], '%s')
                        where_parameters.append("%" + data_value[id] + "%")
                    where_query += " AND " + "(" + temp_query + ")"
                table_no += 1

        with connection.cursor() as cursor:
            if output_format == 'json':
                query = """SELECT count(*) OVER() AS full_count, incident_pk
FROM incidents_incident INNER JOIN custom_user_users ON assigned_to_id = custom_user_users.user_pk INNER JOIN incidents_incidentstatus
    ON (incidents_incident.incident_status_id = incidents_incidentstatus.incident_status_id)%s%s
%s
WHERE resort_id = %d AND custom_user_users.user_connected = 1 AND dt_created IS NOT NULL AND dt_created >= '%s' AND dt_created <= '%s' AND incidents_incidentstatus.order IN (1,2,3,4,5,6,7,8)%s
GROUP BY incident_pk
ORDER BY incidents_incident.dt_created DESC
OFFSET %d
LIMIT %d;""" % (inner_join, from_query, cross_join, resort.resort_pk, dateFrom, dateTo, where_query, offset, chunk)
            elif output_format == 'csv':
                query = """SELECT count(*) OVER() AS full_count, incident_pk
FROM incidents_incident INNER JOIN custom_user_users ON assigned_to_id = custom_user_users.user_pk INNER JOIN incidents_incidentstatus
    ON (incidents_incident.incident_status_id = incidents_incidentstatus.incident_status_id)%s%s
%s
WHERE resort_id = %d AND custom_user_users.user_connected = 1 AND dt_created IS NOT NULL AND dt_created >= '%s' AND dt_created <= '%s' AND incidents_incidentstatus.order IN (1,2,3,4,5,6,7,8)%s
GROUP BY incident_pk
ORDER BY incidents_incident.dt_created DESC;""" % (
                    inner_join, from_query, cross_join, resort.resort_pk, dateFrom, dateTo, where_query)
            cursor.execute(query, where_parameters)
            data = dictfetchall(cursor)

        incident_data = []
        if output_format == 'json':
            for val in data:
                incident_info = IncidentReportSerializer(Incident.objects.get(incident_pk=val['incident_pk']), fields=(
                    'incident_pk', 'incident_id', 'dt_created', 'incident_status', 'assigned_to'), context={'data_key': text_data_key}).data
                incident_data.append(incident_info)

            response_data['offset'] = offset
            response_data['chunk'] = chunk
            response_data['count'] = data[0]['full_count'] if len(data) > 0 else 0
            response_data['results'] = incident_data

        elif output_format == 'csv':
            return sendfile(request, settings.MEDIA_ROOT + dict_to_csv_report(get_report_data_for_csv(data, resort, text_data_key)),
                            attachment=True)

        return Response(response_data, status=200)

    @list_route(methods=['post'])
    def timeline(self, request):
        tempdata = []
        output_format = request.query_params.get('output_format', 'json')

        if request.user.user_connected == 0:
            return Response({_('detail'): _('you do not have access to report')}, status=403)

        resort = get_resort_for_user(request.user)
        text_data_key = get_data_key(resort)
        b = incident_template_field_type_mapping(resort.incident_template)
        datetime_object = extract_date_chart(request.data, resort)

        for idx, value in enumerate(request.data):
            from_query = ''
            where_query = ''
            inner_join = ''
            cross_join = ''
            table_no = 0
            inner_patient = False
            inner_note = False
            group_by_query = ''
            order_by_query = ''
            where_parameter = []
            dateFrom, dateTo = datetime_object[idx]['dateFrom'], datetime_object[idx]['dateTo']
            scale = scale_mapping[value.get('scale', 'date')]

            if scale == 'date':
                column_query = 'incidents_incident.dt_created::TIMESTAMP::DATE as columndetail'
            else:
                if scale in ["hour", "dow"]:
                    column_query = 'extract( ' + scale + ' FROM incidents_incident.dt_created::TIMESTAMP) + 1 as columndetail'
                elif scale == 'hdow':
                    column_query = "extract(DOW FROM incidents_incident.dt_created::TIMESTAMP) + 1 as columndetail, extract( HOUR FROM incidents_incident.dt_created::TIMESTAMP) + 1 as columndetail1"
                    group_by_query = ',columndetail1'
                    order_by_query = ',columndetail1'
                else:
                    column_query = 'extract( ' + scale + ' FROM incidents_incident.dt_created::TIMESTAMP) as columndetail'

            for data_key, data_value in value['data'].iteritems():
                if data_key == 'total_incident':
                    pass
                elif data_key in patient_fields:
                    if not inner_patient:
                        inner_join += ' INNER JOIN incidents_patients ON incidents_patients.incident_id = incidents_incident.incident_pk'
                        cross_join += """CROSS JOIN (SELECT '%s' As datakey) As keys""" % (
                            text_data_key)
                        inner_patient = True
                    for id, value in enumerate(data_value):
                        if data_key in encrypted_fields:
                            where_query += " AND pgp_sym_decrypt(incidents_patients.%s, keys.datakey) ILIKE %s" % (
                                data_key, '%s')
                            where_parameter.append("%" + data_value[id] + "%")
                        elif data_key == 'sex':
                            where_query += " AND incidents_patients.%s = %s" % ('sex', '%s')
                            where_parameter.append(data_value[id].lower())
                        else:
                            where_query += " AND incidents_patients.%s = %s" % (data_key, '%s')
                            where_parameter.append(data_value[id])
                elif data_key in note_fields:
                    if not inner_note:
                        inner_join += ' INNER JOIN incidents_incidentnotes ON incidents_incidentnotes.incident_id = incidents_incident.incident_pk'
                        inner_note = True
                    for id, value in enumerate(data_value):
                        where_query += " AND incidents_incidentnotes.%s = %s" % (
                            note_field_map[data_key], '%s')
                        where_parameter.append(data_value[id])
                elif data_key in location_field:
                    if not 'field_52ca456962ba8' in from_query:
                        from_query += ", CAST((incidents_incident.incident_data -> 'field_52ca456962ba8') AS JSON) as location_json"
                    for id, value in enumerate(data_value):
                        where_query += " AND (location_json ->> '%s') = %s" % (
                            data_key.split('____')[1], '%s')
                        where_parameter.append(data_value[id])
                elif b[data_key]['type'] == 'text' or b[data_key]['type'] == 'int':
                    for id, value in enumerate(data_value):
                        where_query += " AND (incident_data ->> '%s') = %s" % (b[data_key]['key'], '%s')
                        where_parameter.append(data_value[id])
                elif b[data_key]['type'] == 'array':
                    if not b[data_key]['key'] in from_query:
                        from_query += ", json_array_elements(incidents_incident.incident_data -> '%s') as table%d" % (
                            b[data_key]['key'], table_no)
                    for id, value in enumerate(data_value):
                        where_query += " AND CAST(table%d AS TEXT) = %s" % (table_no, '%s')
                        where_parameter.append('"' + data_value[id] + '"')
                    table_no += 1
                elif 'repeating' in b[data_key]['type']:
                    if not b[data_key]['key'] in from_query:
                        from_query += ", CAST(json_array_elements(incidents_incident.incident_data -> '%s') AS JSON) as table%d" % (
                            b[data_key]['key'], table_no)
                    for id, value in enumerate(data_value):
                        where_query += " AND (table%d ->> '%s') = %s" % (
                            table_no, b[data_key]['sub_key'], '%s')
                        where_parameter.append(data_value[id])
            with connection.cursor() as cursor:
                query = """SELECT %d as field, %s , count(*) count
FROM incidents_incident INNER JOIN custom_user_users ON assigned_to_id = custom_user_users.user_pk INNER JOIN incidents_incidentstatus
    ON (incidents_incident.incident_status_id = incidents_incidentstatus.incident_status_id)%s%s
%s
WHERE resort_id = %d AND custom_user_users.user_connected = 1 AND dt_created IS NOT NULL AND dt_created >= '%s' AND dt_created <= '%s' AND incidents_incidentstatus.order IN (1,2,3,4,5,6,7,8)%s
GROUP BY columndetail%s
ORDER BY columndetail%s;""" % (
                idx + 1, column_query, inner_join, from_query, cross_join, resort.resort_pk, dateFrom, dateTo,
                where_query, group_by_query, order_by_query)
                cursor.execute('BEGIN;')
                cursor.execute("SET LOCAL TIME ZONE %s;", [resort.timezone])
                cursor.execute(query, where_parameter)
                data = dictfetchall(cursor)
                cursor.execute('END;')
                tempdata.append(add_missing_data(data, idx + 1, dateFrom, dateTo, scale))

        final_data = merge_compare_data(tempdata)

        if output_format == 'csv':
            scale = scale_mapping[request.data[0].get('scale', 'date')]
            return sendfile(request, settings.MEDIA_ROOT + dict_to_csv_report(final_data, 'timeline', scale),
                            attachment=True)

        return Response(final_data)

    @list_route(methods=['post'])
    def bar(self, request):
        tempdata = []
        output_format = request.query_params.get('output_format', 'json')

        if request.user.user_connected == 0:
            return Response({_('detail'): _('you do not have access to report')}, status=403)

        resort = get_resort_for_user(request.user)
        text_data_key = get_data_key(resort)
        b = incident_template_field_type_mapping(resort.incident_template)
        datetime_object = extract_date_chart(request.data, resort)

        for idx, value in enumerate(request.data):
            from_query = ''
            where_query = ''
            inner_join = ''
            cross_join = ''
            table_no = 0
            inner_patient = False
            inner_note = False
            where_parameter = []
            group_by_query = ''
            order_by_query = ''
            dateFrom, dateTo = datetime_object[idx]['dateFrom'], datetime_object[idx]['dateTo']
            scale = scale_mapping[value.get('scale', 'date')]

            if scale == 'date':
                column_query = 'incidents_incident.dt_created::TIMESTAMP::DATE as columndetail'
            else:
                if scale in ["hour", "dow"]:
                    column_query = 'extract( ' + scale + ' FROM incidents_incident.dt_created::TIMESTAMP) + 1 as columndetail'
                elif scale == 'hdow':
                    column_query = "extract(DOW FROM incidents_incident.dt_created::TIMESTAMP) + 1 as columndetail, extract( HOUR FROM incidents_incident.dt_created::TIMESTAMP) + 1 as columndetail1"
                    group_by_query = ',columndetail1'
                    order_by_query = ',columndetail1'
                else:
                    column_query = 'extract( ' + scale + ' FROM incidents_incident.dt_created::TIMESTAMP) as columndetail'

            for data_key, data_value in value['data'].iteritems():
                if data_key == 'total_incident':
                    pass
                elif data_key in patient_fields:
                    if not inner_patient:
                        inner_join += ' INNER JOIN incidents_patients ON incidents_patients.incident_id = incidents_incident.incident_pk'
                        cross_join += """CROSS JOIN (SELECT '%s' As datakey) As keys""" % (
                            text_data_key)
                        inner_patient = True
                    for id, value in enumerate(data_value):
                        if data_key in encrypted_fields:
                            where_query += " AND pgp_sym_decrypt(incidents_patients.%s, keys.datakey) ILIKE %s" % (
                                data_key, '%s')
                            where_parameter.append("%" + data_value[id] + "%")
                        elif data_key == 'sex':
                            where_query += " AND incidents_patients.%s = %s" % ('sex', '%s')
                            where_parameter.append(data_value[id].lower())
                        else:
                            where_query += " AND incidents_patients.%s = %s" % (data_key, '%s')
                            where_parameter.append(data_value[id])
                elif data_key in note_fields:
                    if not inner_note:
                        inner_join += ' INNER JOIN incidents_incidentnotes ON incidents_incidentnotes.incident_id = incidents_incident.incident_pk'
                        inner_note = True
                    for id, value in enumerate(data_value):
                        where_query += " AND incidents_incidentnotes.%s = %s" % (
                            note_field_map[data_key], '%s')
                        where_parameter.append(data_value[id])
                elif data_key in location_field:
                    if not 'field_52ca456962ba8' in from_query:
                        from_query += ", CAST((incidents_incident.incident_data -> 'field_52ca456962ba8') AS JSON) as location_json"
                    for id, value in enumerate(data_value):
                        where_query += " AND (location_json ->> '%s') = %s" % (
                            data_key.split('____')[1], '%s')
                        where_parameter.append(data_value[id])
                elif b[data_key]['type'] == 'text' or b[data_key]['type'] == 'int':
                    for id, value in enumerate(data_value):
                        where_query += " AND (incident_data ->> '%s') = %s" % (b[data_key]['key'], '%s')
                        where_parameter.append(data_value[id])
                elif b[data_key]['type'] == 'array':
                    if not b[data_key]['key'] in from_query:
                        from_query += ", json_array_elements(incidents_incident.incident_data -> '%s') as table%d" % (
                            b[data_key]['key'], table_no)
                    for id, value in enumerate(data_value):
                        where_query += " AND CAST(table%d AS TEXT) = %s" % (table_no, '%s')
                        where_parameter.append('"' + data_value[id] + '"')
                    table_no += 1
                elif 'repeating' in b[data_key]['type']:
                    if not b[data_key]['key'] in from_query:
                        from_query += ", CAST(json_array_elements(incidents_incident.incident_data -> '%s') AS JSON) as table%d" % (
                            b[data_key]['key'], table_no)
                    for id, value in enumerate(data_value):
                        where_query += " AND (table%d ->> '%s') = %s" % (
                            table_no, b[data_key]['sub_key'], '%s')
                        where_parameter.append(data_value[id])
            with connection.cursor() as cursor:
                query = """SELECT %d as field, %s , count(*) count FROM incidents_incident INNER JOIN custom_user_users ON assigned_to_id = custom_user_users.user_pk INNER JOIN incidents_incidentstatus ON (incidents_incident.incident_status_id = incidents_incidentstatus.incident_status_id)%s %s %s WHERE resort_id = %d AND custom_user_users.user_connected = 1 AND dt_created IS NOT NULL AND dt_created >= '%s' AND dt_created <= '%s' AND incidents_incidentstatus.order IN (1,2,3,4,5,6,7,8) %s GROUP BY columndetail %s ORDER BY columndetail%s;""" % \
                        ( idx + 1, column_query, inner_join, from_query, cross_join, resort.resort_pk, dateFrom, dateTo, where_query, group_by_query, order_by_query)
                cursor.execute('BEGIN;')
                cursor.execute("SET LOCAL TIME ZONE %s;", [resort.timezone])
                cursor.execute(query, where_parameter)
                data = dictfetchall(cursor)
                cursor.execute('END;')
                tempdata.append(add_missing_data(data, idx + 1, dateFrom, dateTo, scale))

        final_data = merge_compare_data(tempdata)

        if output_format == 'csv':
            scale = scale_mapping[request.data[0].get('scale', 'date')]
            return sendfile(request, settings.MEDIA_ROOT + dict_to_csv_report(final_data, 'bar', scale),
                            attachment=True)

        return Response(final_data)

    @list_route(methods=['post'])
    def pie(self, request):
        if request.user.user_connected == 0:
            return Response({_('detail'): _('you do not have access to report')}, status=403)

        response_data = []
        output_format = request.query_params.get('output_format', 'json')

        resort = get_resort_for_user(request.user)
        b = incident_template_field_type_mapping(resort.incident_template)
        datetime_object = extract_date_chart(request.data, resort)
        dateFrom = datetime_object[0]['dateFrom']
        dateTo = datetime_object[0]['dateTo']

        for idx, value in enumerate(request.data):
            dateFrom, dateTo = datetime_object[idx]['dateFrom'], datetime_object[idx]['dateTo']
            key = b[value['data'].keys()[0]]

            for id, val in enumerate(key['data']):
                inner_join = ''
                from_query = ''
                select_query = ''
                where_query = ''
                where_parameter = []
                select_query += "%s as name ,COUNT(*) as count"
                where_parameter.append(val[val.keys()[0]])
                if key['main_type'] == 'gender' or key['key'] == 'country':
                    inner_join += " INNER JOIN incidents_patients on incidents_patients.incident_id = incidents_incident.incident_pk"
                    where_query += " AND incidents_patients.%s = %s" % (key['key'], '%s')
                    where_parameter.append(val.keys()[0])
                elif key['type'] in ['text']:
                    where_query += " AND (incident_data ->> '%s') = %s" % (key['key'], '%s')
                    where_parameter.append(val.keys()[0])
                elif key['type'] == 'array':
                    from_query += ", json_array_elements(incidents_incident.incident_data -> '%s') as table0" % (
                        key['key'])
                    where_query += " AND CAST(table0 AS TEXT) = %s" % ('%s')
                    where_parameter.append('"' + val.keys()[0] + '"')
                elif 'repeating' in key['type']:
                    from_query += ", CAST(json_array_elements(incidents_incident.incident_data -> '%s') AS JSON) as table0" % (
                        key['key'])
                    where_query += " AND (table0 ->> '%s') = %s" % (key['sub_key'], '%s')
                    where_parameter.append(val.keys()[0])

                with connection.cursor() as cursor:
                    query = """SELECT %s
    FROM incidents_incident INNER JOIN custom_user_users ON assigned_to_id = custom_user_users.user_pk INNER JOIN incidents_incidentstatus
    ON (incidents_incident.incident_status_id = incidents_incidentstatus.incident_status_id)%s%s
    WHERE resort_id = %d AND custom_user_users.user_connected = 1 AND dt_created IS NOT NULL AND dt_created >= '%s' AND dt_created <= '%s' AND incidents_incidentstatus.order IN (1,2,3,4,5,6,7,8)%s;""" % (
                        select_query, inner_join, from_query, resort.resort_pk, dateFrom, dateTo, where_query)
                    cursor.execute('BEGIN;')
                    cursor.execute("SET LOCAL TIME ZONE %s;", [resort.timezone])
                    cursor.execute(query, where_parameter)
                    data = dictfetchall(cursor)
                    cursor.execute('END;')

                    response_data.append(data[0])

        cursor = connection.cursor()
        query = """SELECT COUNT(*) as count
FROM incidents_incident INNER JOIN custom_user_users ON assigned_to_id = custom_user_users.user_pk INNER JOIN incidents_incidentstatus
    ON (incidents_incident.incident_status_id = incidents_incidentstatus.incident_status_id)
WHERE resort_id = %d AND custom_user_users.user_connected = 1 AND dt_created IS NOT NULL AND dt_created >= '%s' AND dt_created <= '%s' AND incidents_incidentstatus.order IN (1,2,3,4,5,6,7,8);""" % (
            resort.resort_pk, dateFrom, dateTo)

        cursor.execute(query)
        total_data = dictfetchall(cursor)
        final_data = process_pie_chart_data(response_data, total_data[0]['count'])

        if output_format == 'csv':
            return sendfile(request, settings.MEDIA_ROOT + dict_to_csv_report(final_data), attachment=True)

        return Response(final_data)


class StatusIncidentAPIView(ListAPIView):

    def get(self, request, *args, **kwargs):
        if request.user.user_connected == 0:
            return Response({_('detail'): _('you do not have access to report')}, status=403)

        output_format = request.query_params.get('output_format', 'json')
        include_status = map(int, request.query_params.get('status', '1,2,3,4,5,6,7,8').split(','))
        datefrom, dateto, resort = get_param(request)
        query = Incident.objects.filter(resort__resort_id=resort.resort_id, dt_created__gte=datefrom, dt_created__lte=dateto, incident_status__order__in=include_status).order_by('-dt_created')

        incident_status_data = incident_status_grouping(query, include_status)

        queryset = self.filter_queryset(query)

        if output_format == 'json':
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = IncidentStatusReportSerializer(page, fields=(
                'incident_pk', 'incident_id', 'dt_created', 'incident_status', 'assigned_to'),
                                                many=True)
                response = self.get_paginated_response(serializer.data)
                response.data.update({'summary': incident_status_data})
                return response

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        elif output_format == 'csv':
            serializer = IncidentStatusReportSerializer(query, fields=(
                'incident_pk', 'incident_id', 'dt_created', 'incident_status', 'assigned_to'),
                                                many=True)
            csv_data = []
            local_tz = pytz.timezone(resort.timezone)
            for each_data in serializer.data:
                temp_dict = OrderedDict()
                temp_dict.update({'incident id': each_data['incident_pk']})
                temp_dict.update({'date': pytz.utc.localize(
                    datetime.strptime(each_data['dt_created'], '%Y-%m-%d %H:%M:%S'), is_dst=None).astimezone(
                    local_tz).strftime(date_mapping[resort.datetime_format])})
                temp_dict.update(
                    {'location': _(each_data['location']['area_name']) + " " + _(each_data['location']['run_name'])})
                temp_dict.update({'injury': transform_injury_repeater(each_data['injury'])})
                temp_dict.update({'responder': _(each_data['assigned_to']['name'])})
                temp_dict.update({'response': _(each_data['referred_to'])})
                temp_dict.update({'status': _(each_data['incident_status']['status_label'])})
                csv_data.append(temp_dict)

            return sendfile(request, settings.MEDIA_ROOT + dict_to_csv_report(csv_data),
                            attachment=True)