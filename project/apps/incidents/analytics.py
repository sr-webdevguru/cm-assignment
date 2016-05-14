import base64
from datetime import datetime, date

from django.conf import settings
from django.db import connection
from django.utils.translation import ugettext as _
from rest_framework import viewsets
from rest_framework.response import Response

from apps.custom_user.utils import get_roleid_user
from apps.incidents.utils import dictfetchall, get_data_key
from apps.resorts.models import Resort
from apps.resorts.utils import get_resort_for_user


def get_param(request):
    dateFrom = request.GET.get('datefrom', None)
    if dateFrom is None:
        dateFrom = datetime.today()
        dateFrom = dateFrom.strftime("%Y-%m-%d 00:00:00")
    else:
        dateFrom = (datetime.strptime(str(dateFrom), "%Y-%m-%d %H:%M:%S"))
        dateFrom = dateFrom.strftime("%Y-%m-%d 00:00:00")
    dateTo = request.GET.get('dateto', None)
    if dateTo is None or not dateTo:
        dateTo = datetime.today()
        dateTo = dateTo.strftime("%Y-%m-%d 23:59:59")
    else:
        dateTo = (datetime.strptime(dateTo, "%Y-%m-%d %H:%M:%S"))
        dateTo = dateTo.strftime("%Y-%m-%d 23:59:59")

    resort_id = request.GET.get('resort_id', None)

    try:
        resort = Resort.objects.get(resort_id=resort_id)
    except:
        resort = get_resort_for_user(user=request.user)

    return dateFrom, dateTo, resort


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


class AnalyticsViewSet(viewsets.ViewSet):
    def gender(self, request):
        dateFrom, dateTo, resort = get_param(request)

        user_role = get_roleid_user(resort, request.user)

        if user_role == 1:
            return Response({_("detail"): _("You do not have permission to view analytics")}, status=403)

        with connection.cursor() as cursor:
            cursor.execute("""SELECT
  extract(year from incidents_incident.dt_created) as year,
  extract(month from incidents_incident.dt_created) as month,
  SUM(CASE WHEN incidents_patients.sex  = 'male' then 1 else 0 end) as Male,
  SUM(CASE WHEN incidents_patients.sex = 'female' then 1 else 0 end) as Female,
  SUM(CASE WHEN incidents_patients.sex = '' then 1 else 0 end) as Unknown
FROM
  incidents_incident
LEFT JOIN incidents_patients ON incidents_incident.incident_pk = incidents_patients.incident_id
INNER JOIN custom_user_users ON assigned_to_id = custom_user_users.user_pk
WHERE
  incidents_incident.resort_id = %d
  AND custom_user_users.user_connected = %d
  AND incidents_incident.dt_created IS NOT NULL AND incidents_incident.dt_created >= '%s' AND incidents_incident.dt_created <= '%s'
  AND incidents_incident.incident_status_id <> 9
GROUP BY 1,2
ORDER BY 1,2;""" % (resort.resort_pk, request.user.user_connected, dateFrom, dateTo))

            data = dictfetchall(cursor)

        return Response({
            'success': True,
            'data': data
        }, status=200)

    def injury_types(self, request):
        dateFrom, dateTo, resort = get_param(request)

        user_role = get_roleid_user(resort, request.user)

        if user_role == 1:
            return Response({_("detail"): _("You do not have permission to view analytics")}, status=403)

        with connection.cursor() as cursor:
            cursor.execute("""SELECT
  injury_types->>'injury_type' as injury,
  COUNT(injury_types->'injury_type') as num
FROM
  incidents_incident INNER JOIN custom_user_users ON custom_user_users.user_pk = incidents_incident.assigned_to_id,
  json_array_elements(incidents_incident.incident_data -> 'field_52d4798f6d227') as injury_types
WHERE
  resort_id = %d
  AND custom_user_users.user_connected = %d
  AND dt_Created IS NOT NULL AND dt_Created >= '%s' AND dt_Created <= '%s'
  AND incidents_incident.incident_status_id <> 9
GROUP BY injury_types->>'injury_type';""" % (resort.resort_pk, request.user.user_connected, dateFrom, dateTo))

            data = dictfetchall(cursor)

        return Response({
            'success': True,
            'data': data
        }, status=200)

    def activity(self, request):
        dateFrom, dateTo, resort = get_param(request)

        user_role = get_roleid_user(resort, request.user)

        if user_role == 1:
            return Response({_("detail"): _("You do not have permission to view analytics")}, status=403)

        with connection.cursor() as cursor:
            cursor.execute("""SELECT
  incidents_incident.incident_data->>'field_52ca3dc8ac437' as activity,
  COUNT(incidents_incident.incident_data->>'field_52ca3dc8ac437') as num,
  ROUND((COUNT(incidents_incident.incident_data->>'field_52ca3dc8ac437')*100.0)/(SELECT CASE count(*) WHEN 0 THEN 1 ELSE count(*) END AS  total FROM incidents_incident WHERE resort_id = %s AND CAST(incidents_incident.incident_data->>'field_52ca3dc8ac437' AS integer)>0 AND dt_created >= %s AND dt_created <= %s AND incident_status_id <> 9)) as percent,
  (SELECT COUNT(*) AS  total FROM incidents_incident WHERE resort_id = %s AND CAST(incidents_incident.incident_data->>'field_52ca3dc8ac437' AS integer) > 0 AND dt_created >= %s AND dt_created <= %s AND incident_status_id <> 9) as total
FROM incidents_incident
INNER JOIN custom_user_users ON custom_user_users.user_pk = incidents_incident.assigned_to_id
WHERE resort_id = %s AND custom_user_users.user_connected = %s AND CAST(incidents_incident.incident_data->>'field_52ca3dc8ac437' AS integer) > 0 AND dt_created IS NOT NULL AND dt_created >= %s AND dt_created <= %s AND incidents_incident.incident_status_id <> 9
GROUP BY 1;""", [resort.resort_pk, dateFrom, dateTo, resort.resort_pk, dateFrom, dateTo, resort.resort_pk,
                 request.user.user_connected, dateFrom, dateTo])

            data = dictfetchall(cursor)

        return Response({
            'success': True,
            'data': data
        }, status=200)

    def referred_to(self, request):
        dateFrom, dateTo, resort = get_param(request)

        user_role = get_roleid_user(resort, request.user)

        if user_role == 1:
            return Response({_("detail"): _("You do not have permission to view analytics")}, status=403)

        with connection.cursor() as cursor:
            cursor.execute("""SELECT
  incident_data ->>'field_52d48077a16be' AS referred_to ,
  COUNT(incident_data->>'field_52d48077a16be') AS num,
  ROUND((COUNT(incident_data->>'field_52d48077a16be')*100.0)/(SELECT CASE COUNT(*) WHEN 0 THEN 1 ELSE COUNT(*) END AS  total FROM incidents_incident WHERE resort_id = %s AND CAST(incidents_incident.incident_data->>'field_52d48077a16be' AS integer)>0 AND dt_created >= %s AND dt_created <= %s AND incident_status_id <> 9)) AS percent,
  (SELECT COUNT(*) AS  total FROM incidents_incident WHERE resort_id = %s AND CAST(incident_data->>'field_52d48077a16be' AS integer) > 0 AND dt_created >= %s AND dt_created <= %s AND incident_status_id <> 9)
FROM incidents_incident
INNER JOIN custom_user_users ON custom_user_users.user_pk = incidents_incident.assigned_to_id
WHERE resort_id = %s AND custom_user_users.user_connected = %s AND CAST(incident_data->>'field_52d48077a16be' AS integer) > 0  AND dt_created IS NOT NULL AND dt_created >= %s AND dt_created <= %s AND incident_status_id <> 9
GROUP BY 1;""", [resort.resort_pk, dateFrom, dateTo, resort.resort_pk, dateFrom, dateTo, resort.resort_pk,
                 request.user.user_connected, dateFrom, dateTo])

            data = dictfetchall(cursor)

        return Response({
            'success': True,
            'data': data
        }, status=200)

    def age(self, request):

        dateFrom, dateTo, resort = get_param(request)

        user_role = get_roleid_user(resort, request.user)

        if user_role == 1:
            return Response({_("detail"): _("You do not have permission to view analytics")}, status=403)

        data_key = get_data_key(resort)

        with connection.cursor() as cursor:
            cursor.execute("""SELECT
  SUM(case when age_years>=0 and age_years <= 10 then 1 else 0 end) AS G0_10,
  SUM(case when age_years>=11 and age_years <= 15 then 1 else 0 end) AS G11_15,
  SUM(case when age_years>=16 and age_years <= 18 then 1 else 0 end) AS G16_18,
  SUM(case when age_years>=19 and age_years <= 21 then 1 else 0 end) AS G19_21,
  SUM(case when age_years>=22 and age_years <= 30 then 1 else 0 end) AS G22_30,
  SUM(case when age_years>=31 and age_years <= 100 then 1 else 0 end) AS G31_
FROM incidents_incident INNER JOIN custom_user_users ON custom_user_users.user_pk = incidents_incident.assigned_to_id, incidents_patients, date_part('year',age(to_timestamp(pgp_sym_decrypt(incidents_patients.dob, '%s'::TEXT),'YYYYMMDD'))) as age_years
WHERE incidents_incident.incident_pk = incidents_patients.incident_id
AND incidents_incident.resort_id = %d AND custom_user_users.user_connected = %d AND incidents_incident.dt_created IS NOT NULL
AND incidents_incident.dt_created >= '%s' AND incidents_incident.dt_created <= '%s'
AND incidents_incident.incident_status_id <> 9;""" % (
            data_key, resort.resort_pk, request.user.user_connected, dateFrom, dateTo))

            data = dictfetchall(cursor)

        return Response({
            'success': True,
            'data': data[0]
        }, status=200)

    def alcohol(self, request):
        dateFrom, dateTo, resort = get_param(request)

        user_role = get_roleid_user(resort, request.user)

        if user_role == 1:
            return Response({_("detail"): _("You do not have permission to view analytics")}, status=403)

        with connection.cursor() as cursor:
            cursor.execute("""SELECT
  extract(year from dt_created) as year,
  extract(month from dt_created) as month,
  SUM(case when incidents_incident.incident_data->>'field_52ca437b62b9c' = 'yes' then  1 else 0 end) as drugs,
  SUM(case when incidents_incident.incident_data->>'field_52ca3fcc59d29' = 'yes' then  1 else 0 end) as alcohol
FROM incidents_incident
INNER JOIN custom_user_users ON custom_user_users.user_pk = incidents_incident.assigned_to_id
WHERE resort_id = %d AND custom_user_users.user_connected = %d AND dt_Created IS NOT NULL AND dt_created >= '%s' AND dt_created <= '%s' AND incidents_incident.incident_status_id <> 9
GROUP BY 1,2
ORDER BY 1,2;""" % (resort.resort_pk, request.user.user_connected, dateFrom, dateTo))

            data = dictfetchall(cursor)

        return Response({
            'success': True,
            'data': data
        }, status=200)

    def patrollers(self, request):
        dateFrom, dateTo, resort = get_param(request)

        user_role = get_roleid_user(resort, request.user)

        if user_role == 1:
            return Response({_("detail"): _("You do not have permission to view analytics")}, status=403)

        with connection.cursor() as cursor:
            cursor.execute("""SELECT
  json_array_elements(CAST (resorts_resort.incident_template AS JSON)->'DashboardItems'->'field_52d47aac9bd13'->'RepeatingQuestions'->'patroller'->'Values') ->> (patrollers_incident->>'patroller') as name,
  SUM(CASE WHEN CAST (patrollers_incident->'incident_role' AS text) = '"170"' THEN 1 ELSE 0 END) AS "primary",
  SUM(CASE WHEN CAST (patrollers_incident->'incident_role' AS text) = '"171"' THEN 1 ELSE 0 END) AS secondary,
  SUM(CASE WHEN CAST (patrollers_incident->'incident_role' AS text) = '"172"' THEN 1 ELSE 0 END) AS assist
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
GROUP BY 1;""" % (resort.resort_pk, request.user.user_connected, resort.resort_pk, dateFrom, dateTo))

            data = dictfetchall(cursor)

            if data:
                data.pop(0)

        return Response({
            'success': True,
            'data': data
        }, status=200)


gender = AnalyticsViewSet.as_view({'get': 'gender'})
injury_types = AnalyticsViewSet.as_view({'get': 'injury_types'})
activity = AnalyticsViewSet.as_view({'get': 'activity'})
referred_to = AnalyticsViewSet.as_view({'get': 'referred_to'})
age = AnalyticsViewSet.as_view({'get': 'age'})
alcohol = AnalyticsViewSet.as_view({'get': 'alcohol'})
patrollers = AnalyticsViewSet.as_view({'get': 'patrollers'})
