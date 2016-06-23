import csv
import datetime as dt
import json
import os
import uuid
from collections import OrderedDict
from datetime import datetime, timedelta

from django.conf import settings
from django.db import connection
from django.utils.translation import ugettext
from pytz import timezone
from django.utils.translation import ugettext as _

from apps.incidents.models import IncidentStatus
from apps.incidents.serializers import IncidentStatusSerializer
from apps.incidents.utils import dictfetchall
from apps.incidents.utils import get_full_incident
from apps.incidents.utils import get_patient_info
from apps.resorts.utils import get_resort_for_user

field_type_mapping = {
    "text": "text",
    "radio": "text",
    "radio_button": "text",
    "number": "int",
    "multi_select": "array",
    "image": "text",
    "google_map": "nested special case",
    "select": "text",
    "signature": "text",
    "textarea": "text",
    "date_time_picker": "text",
    "message": "text",
    "range": "text",
    "gender": "text",
    "timer": "text",
    "date_picker": "text",
    "hidden": "text",
    "file": "text",
    "arrows": "text",
    "email": "text",
    "decimal": "int",
    "patient_age": "int",
    "temperature": "int",
    "weight": "int",
    "height": "int",
    "distance": "int",
    "length": "int",
    "altitude": "int"
}

scale_limit_mapping = {
    "day": 31,
    "hour": 24,
    "dow": 7,
    "week": 52,
    "month": 12
}

DAY_NAME = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
MONTH_NAME = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']


def create_report(status, user, config, resort):
    with connection.cursor() as cursor:
        cursor.execute("""INSERT INTO reports_report (
            report_id,
            global_status,
            report_user,
            report_config,
            report_resort
        ) VALUES (
            uuid_generate_v4(),
            %s,
            %s,
            %s,
            %s
        )
        RETURNING report_id, report_config;
        """, [status, user.user_pk, json.dumps(config), resort.resort_pk])
        data = dictfetchall(cursor)
        cursor.close()
        return data[0]


def update_report(status, user, config, report_id):
    with connection.cursor() as cursor:
        cursor.execute("""UPDATE reports_report SET
            global_status = %s,
            report_user = %s,
            report_config = %s
            WHERE report_id = %s
            RETURNING report_id, report_config;""", [status, user.user_pk, json.dumps(config), report_id])
        data = dictfetchall(cursor)
        cursor.close()
    return data[0]


def get_report(report_id):
    with connection.cursor() as cursor:
        cursor.execute("""SELECT report_id, report_config
            FROM reports_report
            WHERE report_id = %s;""", [report_id])
        data = dictfetchall(cursor)
    return data[0]


def list_report(user):
    resort = get_resort_for_user(user)
    with connection.cursor() as cursor:
        cursor.execute("""SELECT report_id as report_id, (report_config ->> 'label') as label, global_status as global, (report_config ->> 'type') as type
            FROM reports_report
            WHERE report_resort = %s AND (report_user = %s OR global_status = 1) ;""", [resort.resort_pk, user.user_pk])
        data = dictfetchall(cursor)
    return data


def dict_to_csv_report(incident_data, datatype=None, scale=None):
    outval = []

    if datatype in ['timeline', 'bar']:
        for index, val in enumerate(incident_data):
            inner_outval = OrderedDict()
            for index1, val1 in enumerate(val):
                for key2, val2 in val1.iteritems():
                    if key2 != 'field':
                        if key2 == 'columndetail':
                            inner_outval.update({scale + '-' + str(index1 + 1): val2})
                        else:
                            inner_outval.update({key2 + '-' + str(index1 + 1): val2})
            outval.append(inner_outval)
    else:
        for index, val in enumerate(incident_data):
            b = OrderedDict()
            for key, value in val.iteritems():
                if isinstance(value, dict):
                    for key1, value1 in value.iteritems():
                        b.update({key1: value1})

                elif isinstance(value, list):
                    if value:
                        if isinstance(value[0], dict):
                            for key2, value2 in value[0].iteritems():
                                b.update({key2: value2})
                    else:
                        b.update({key: ""})
                else:
                    b.update({key: value})
            outval.append(b)

    csv_path = os.path.join(settings.MEDIA_ROOT, 'media', 'tmp')
    file_name = str(uuid.uuid4()) + '.csv'
    csv_send_file = '/media' + os.path.join(csv_path.split('/media')[1], file_name)

    if not os.path.exists(csv_path):
        os.makedirs(csv_path)

    with open(os.path.join(csv_path, file_name), 'wb') as output:
        w = csv.DictWriter(output, outval[0].keys())
        w.writeheader()
        w.writerows(outval)

    return csv_send_file


# Calculates the days between 2 dates.
# First parameter -> Start date
# Second parameter -> End date
def days_between_two_dates(date1, date2):
    return (date2 - date1).days + 2


def extract_date_chart(data, resort):
    datefrom_1 = datetime.strptime(data[0]['date'].get('datefrom'), "%Y-%m-%d %H:%M:%S")
    dateto_1 = datetime.strptime(data[0]['date'].get('dateto'), "%Y-%m-%d %H:%M:%S")
    datefrom_1 = timezone('UTC').localize(datefrom_1)
    datefrom_1 = datefrom_1.astimezone(timezone(resort.timezone))
    dateto_1 = timezone('UTC').localize(dateto_1)
    dateto_1 = dateto_1.astimezone(timezone(resort.timezone))
    total_days = days_between_two_dates(datefrom_1, dateto_1)

    date_object = []
    for id, val in enumerate(data):
        temp_data = {}
        if id == 0:
            temp_data = {"dateFrom": datefrom_1, "dateTo": dateto_1}
        else:
            datefrom_1 = datetime.strptime(data[id]['date'].get('datefrom'), "%Y-%m-%d %H:%M:%S")
            dateto_1 = datetime.strptime(data[id]['date'].get('dateto'), "%Y-%m-%d %H:%M:%S")

            datefrom_1 = timezone('UTC').localize(datefrom_1)
            datefrom_1 = datefrom_1.astimezone(timezone(resort.timezone))
            dateto_1 = timezone('UTC').localize(dateto_1)
            dateto_1 = dateto_1.astimezone(timezone(resort.timezone))

            total_days_1 = days_between_two_dates(datefrom_1, dateto_1)
            day_difference = total_days - total_days_1

            if day_difference > 0:
                dateto_1 += timedelta(days=day_difference)
            elif day_difference < 0:
                dateto_1 -= timedelta(days=day_difference)

            temp_data = {"dateFrom": datefrom_1, "dateTo": dateto_1}

        date_object.append(temp_data)

    return date_object


def incident_template_field_type_mapping(incident_template):
    mapped_template = {}

    for key, value in incident_template['DashboardItems'].iteritems():
        if value.has_key('RepeatingQuestions'):
            for inner_key, inner_value in value['RepeatingQuestions'].iteritems():
                mapped_template.update({key + '____' + inner_key: {'key': "%s" % (key,), 'sub_key': "%s" % (inner_key,),
                                                                   'type': field_type_mapping[
                                                                               inner_value['Type']] + '-repeating',
                                                                   'main_type': inner_value['Type'],
                                                                   'data': inner_value['Values'] if inner_value[
                                                                                                        'Type'] in [
                                                                                                        'select',
                                                                                                        'multi_select',
                                                                                                        'radio',
                                                                                                        'radio_button',
                                                                                                        'gender',
                                                                                                        'arrows'] else []
                                                                   }})
        elif value.has_key('Questions'):
            for inner_key1, inner_value1 in value['Questions'].iteritems():
                if inner_value1.has_key('RepeatingQuestions'):
                    for inner_key2, inner_value2 in inner_value1['RepeatingQuestions'].iteritems():
                        mapped_template.update({
                            inner_key1 + '____' + inner_key2: {'key': "%s" % (inner_key1,),
                                                               'sub_key': "%s" % (inner_key2,),
                                                               'type': field_type_mapping[
                                                                           inner_value2['Type']] + '-repeating',
                                                               'main_type': inner_value2['Type'],
                                                               'data': inner_value2['Values'] if inner_value2[
                                                                                                     'Type'] in [
                                                                                                     'select',
                                                                                                     'multi_select',
                                                                                                     'radio',
                                                                                                     'radio_button', 'gender',
                                                                                                     'arrows'] else []
                                                               }})
                else:
                    mapped_template.update({
                        inner_key1: {'key': "%s" % (inner_key1,),
                                     'type': field_type_mapping[inner_value1['Type']],
                                     'main_type': inner_value1['Type'],
                                     'data': inner_value1['Values'] if inner_value1['Type'] in ['select',
                                                                                                'multi_select',
                                                                                                'radio',
                                                                                                'radio_button',
                                                                                                'gender',
                                                                                                'arrows'] else []
                                     }})
    return mapped_template


def process_data_for_hour_of_day_of_week(data):
    field = data[0]['field']
    data_sorting = {}
    for value in data:
        if value['columndetail'] in data_sorting:
            existing_data = data_sorting[value['columndetail']]
            existing_data.append(value['columndetail1'])
        else:
            data_sorting.update({value['columndetail']: [value['columndetail1']]})

    final_data = []
    data_count = 0
    for i in range(1, 8):
        if i in data_sorting:
            temp_data = data_sorting[i]
            for j in range(1, 25):
                if j in temp_data:
                    final_data.append({
                        'count': data[data_count]['count'],
                        'field': field,
                        'columndetail': "%s %d" % (
                        DAY_NAME[int(data[data_count]['columndetail']) - 1], int(data[data_count]['columndetail1']))
                    })
                    data_count += 1
                else:
                    final_data.append({
                        'count': 0,
                        'field': field,
                        'columndetail': "%s %d" % (DAY_NAME[i - 1], j)
                    })
        else:
            for j in range(1, 25):
                final_data.append({
                    'count': 0,
                    'field': field,
                    'columndetail': "%s %d" % (DAY_NAME[i - 1], j)
                })
    return final_data


def add_missing_data(data, idx, start_date, end_date, scale):
    return_list = []
    start_date = start_date.date()
    end_date = end_date.date()
    if scale == 'date':
        days = (end_date - start_date).days

        temp_count = 0
        for id1 in range(0, days + 1):
            if temp_count < len(data):
                if str(data[temp_count]['columndetail']) != str(start_date):
                    temp_dict = OrderedDict()
                    temp_dict.update({"field": idx})
                    temp_dict.update({"columndetail": str(start_date)})
                    temp_dict.update({"count": 0})
                    return_list.append(temp_dict)
                else:
                    return_list.append(data[temp_count])
                    temp_count += 1
            else:
                temp_dict = OrderedDict()
                temp_dict.update({"field": idx})
                temp_dict.update({"columndetail": str(start_date)})
                temp_dict.update({"count": 0})
                return_list.append(temp_dict)
            start_date += dt.timedelta(days=1)
    elif scale == 'hdow':
        return process_data_for_hour_of_day_of_week(data)
    else:
        start_val = 0
        end_val = 0
        difference_val = 0
        if scale == 'year':
            start_val = start_date.year
            end_val = end_date.year
        else:
            start_val = 1
            end_val = scale_limit_mapping[scale]
        difference_val = end_val - start_val + 1
        temp_count = 0
        for id2 in range(0, difference_val):
            if temp_count < len(data):
                if data[temp_count]['columndetail'] != start_val:
                    temp_dict = OrderedDict()
                    temp_dict.update({"field": idx})

                    if scale == 'dow':
                        temp_dict.update({"columndetail": DAY_NAME[start_val - 1]})
                    elif scale == 'month':
                        temp_dict.update({"columndetail": MONTH_NAME[start_val - 1]})
                    else:
                        temp_dict.update({"columndetail": start_val})

                    temp_dict.update({"count": 0})
                    return_list.append(temp_dict)
                else:
                    if scale == 'dow':
                        data[temp_count]["columndetail"] = DAY_NAME[start_val - 1]
                    elif scale == 'month':
                        data[temp_count]["columndetail"] = MONTH_NAME[start_val - 1]

                    return_list.append(data[temp_count])
                    temp_count += 1
            else:
                temp_dict = OrderedDict()
                temp_dict.update({"field": idx})

                if scale == 'dow':
                    temp_dict.update({"columndetail": DAY_NAME[start_val - 1]})
                elif scale == 'month':
                    temp_dict.update({"columndetail": MONTH_NAME[start_val - 1]})
                else:
                    temp_dict.update({"columndetail": start_val})

                temp_dict.update({"count": 0})
                return_list.append(temp_dict)
            start_val += 1

    return return_list


def merge_compare_data(data):
    main_data = []
    for idx in range(0, len(data[0])):
        temp_data = []
        for id in range(0, len(data)):
            temp_data.append(data[id][idx])
        main_data.append(temp_data)

    return main_data


def process_pie_chart_data(data, total):
    data_total = 0
    for id, value in enumerate(data):
        data_total += value['count']

    # data.append({"name": "Unknown", "count": total-data_total})
    return data


def get_report_data_for_csv(incident_data, resort, data_key):
    response_data = []
    resort_timezone = timezone(resort.timezone)

    # Get the different list of values from resort incident config
    config = resort.incident_template
    try:
        referred_to_raw = config['DashboardItems']['field_52ca42770a179']['Questions']['field_52d48077a16be']['Values']
        referred_to = {}
        for value4 in referred_to_raw:
            referred_to.update(value4)
    except:
        pass

    try:
        activity_raw = config['DashboardItems']['field_52ca41790a16c']['Questions']['field_52ca3dc8ac437']['Values']
        activity = {}
        for value5 in activity_raw:
            activity.update(value5)
    except:
        pass
    
    try:
        ability_raw = config['DashboardItems']['field_52ca41790a16c']['Questions']['field_52ca3dfcac438']['Values']
        ability = {}
        for value6 in ability_raw:
            ability.update(value6)
    except:
        pass

    try:
        ability_raw = config['DashboardItems']['field_52ca41790a16c']['Questions']['field_52ca3dfcac438']['Values']
        ability = {}
        for value6 in ability_raw:
            ability.update(value6)
    except:
        pass

    try:
        injuries_json = config['DashboardItems']['field_52d4798f6d229']['Questions']['field_52d4798f6d227'][
            'RepeatingQuestions']
    except:
        pass

    try:
        injury_location_values_raw = injuries_json['injury_location']['Values']
        injury_location_values = {}
        for value6 in injury_location_values_raw:
            injury_location_values.update(value6)
    except:
        pass

    try:
        body_part_values_raw = injuries_json['body_part']['Values']
        body_part_values = {}
        for value7 in body_part_values_raw:
            body_part_values.update(value7)
    except:
        pass

    try:
        injury_type_values_raw = injuries_json['injury_type']['Values']
        injury_type_values = {}
        for value8 in injury_type_values_raw:
            injury_type_values.update(value8)
    except:
        pass

    try:
        incident_type_raw = config['DashboardItems']['field_52ca419f0a16e']['Questions']['field_52ca447762ba2'][
            'Values']
        type_of_incident = {}
        for value in incident_type_raw:
            type_of_incident.update(value)
    except:
        pass

    try:
        treatment_raw = config['DashboardItems']['field_52ca42230a171']['Questions']['field_52ca445d62ba1']['Values']
        treatment = {}
        for value1 in treatment_raw:
            treatment.update(value1)
    except:
        pass

    try:
        transport_raw = config['DashboardItems']['field_52ca425e0a176']['Questions']['field_52ca4c34ef1a1']['Values']
        transport = {}
        for value2 in transport_raw:
            transport.update(value2)
    except:
        pass

    try:
        drug_administred_raw = \
        config['DashboardItems']['field_52ca42230a171']['Questions']['field_52d4800164f2e']['RepeatingQuestions'][
            'drug_administered']['Values']
        drug_administred = {}
        for value3 in drug_administred_raw:
            drug_administred.update(value3)
    except:
        pass

    for val in incident_data:
        single_incident_data = OrderedDict()
        incident_data = get_full_incident(val['incident_pk'])
        single_incident_data['incident id'] = incident_data[
            'incident_sequence'] if resort.use_sequential_incident_id else str(incident_data['incident_pk'])
        single_incident_data['Date and Time of incident '] = incident_data['dt_created'].astimezone(
            resort_timezone).strftime('%Y-%m-%d %H:%M:%S')

        patient = get_patient_info(val['incident_pk'], data_key)
        single_incident_data['Sex'] = patient['sex']
        single_incident_data['DOB'] = patient['dob']

        try:
            single_incident_data['Outcome'] = ugettext(
                referred_to[incident_data['incident_data']['field_52d48077a16be']])
        except:
            single_incident_data['Outcome'] = ''

        try:
            single_incident_data['Activity'] = ugettext(activity[incident_data['incident_data']['field_52ca3dc8ac437']])
        except:
            single_incident_data['Activity'] = ''

        # Injury data
        try:
            injury_info = incident_data['incident_data']['field_52d4798f6d227']
            injury_location = ""
            body_part = ""
            injury_type = ""

            try:
                injury_type_key = injury_info[0]['injury_type']
                single_incident_data['Type of injury sustained'] = ugettext(injury_type_values[injury_type_key])
            except:
                single_incident_data['Type of injury sustained'] = ""

            try:
                body_part_key = injury_info[0]['body_part']
                single_incident_data['body part'] = ugettext(body_part_values[body_part_key])
            except:
                single_incident_data['body part'] = ""

            try:
                injury_location_key = injury_info[0]['injury_location']
                single_incident_data['location'] = ugettext(injury_location_values[injury_location_key])
            except:
                single_incident_data['location'] = ""


            try:
                injury_type_key = injury_info[0]['injury_type']
                single_incident_data['Possible Injury'] = ugettext(injury_type_values[injury_type_key])
            except:
                single_incident_data['Possible Injury'] = ""


        except:
            single_incident_data['Type of injury sustained'] = ""
            single_incident_data['body part'] = ""
            single_incident_data['location'] = ""
            single_incident_data['Possible Injury'] = ""

        # location data
        try:
            area_name = incident_data['incident_data']['field_554f7cbb3d784']
        except:
            area_name = ""

        try:
            location_info = incident_data['incident_data']['field_551c8aaa3d786']
        except:
            location_info = ""

        single_incident_data['area name'] = area_name
        single_incident_data['location info'] = location_info
        
        try:
            single_incident_data['Ability'] = ugettext(ability[incident_data['incident_data']['field_52ca3dfcac438']])
        except:
            single_incident_data['Ability'] = ''

        try:
            lift_name = incident_data['incident_data']['field_52dabradbe3']
            single_incident_data['Lift Name'] = lift_name
        except:
            single_incident_data['Lift Name'] = ""

        try:
            single_incident_data['Ability'] = ugettext(ability[incident_data['incident_data']['field_52ca3dfcac438']])
        except:
            single_incident_data['Ability'] = ''

        try:
            lift_name = incident_data['incident_data']['field_52dabradbe3']
            single_incident_data['Lift Name'] = lift_name
        except:
            single_incident_data['Lift Name'] = ""

        # Type of incident
        try:
            incident_type = incident_data['incident_data']['field_52ca447762ba2']
            incident_type_string = ""
            for id1, val1 in enumerate(incident_type):
                if id1 == 0:
                    incident_type_string = ugettext(type_of_incident[val1])
                else:
                    incident_type_string += ', ' + ugettext(type_of_incident[val1])
            single_incident_data['Mechanism of injury'] = incident_type_string
        except:
            single_incident_data['Mechanism of injury'] = ""

        # Treatment
        try:
            incident_treatment = incident_data['incident_data']['field_52ca445d62ba1']
            treatment_given = ""
            for id2, val2 in enumerate(incident_treatment):
                if id2 == 0:
                    treatment_given += ugettext(treatment[val2])
                else:
                    treatment_given += ', ' + ugettext(treatment[val2])
            single_incident_data['Treatment given'] = treatment_given
        except:
            single_incident_data['Treatment given'] = ""

        # # Drug administrated
        try:
            incident_drug_administred = incident_data['incident_data']['field_52d4800164f2e']
            drug_administred_key = incident_drug_administred[0]['drug_administered']
            single_incident_data['Drug Administered'] = ugettext(drug_administred[drug_administred_key])
        except:
            single_incident_data['Drug Administered'] = ""

        # Transport used
        try:
            incident_transport = incident_data['incident_data']['field_52ca4c34ef1a1']
            transport_used = ""
            for id3, val3 in enumerate(incident_transport):
                if id3 == 0:
                    transport_used += ugettext(transport[val3])
                else:
                    transport_used += ', ' + ugettext(transport[val3])
            single_incident_data['Transport used for on-hill evacuation'] = transport_used
        except:
            single_incident_data['Transport used for on-hill evacuation'] = ""

        # Helmet worn
        try:
            helmet_worn = incident_data['incident_data']['field_52ca430462b9a']
            single_incident_data['Helmet worn'] = ugettext(helmet_worn)
        except:
            single_incident_data['Helmet worn'] = ""

        # Wrist guards
        try:
            wrist_guards = incident_data['incident_data']['field_52ca429c62b98']
            single_incident_data['Wrist guards'] = ugettext(wrist_guards)
        except:
            single_incident_data['Wrist guards'] = ""

        response_data.append(single_incident_data)
    return response_data


def incident_status_grouping(incident_data, include_status):

    all_incident_status = IncidentStatus.objects.filter(order__in=include_status).order_by('order')
    incident_status = IncidentStatusSerializer(all_incident_status, fields=('key', 'order'), many=True)

    incident_status_group = incident_status.data

    temp_status_data = {}
    for data in incident_data:
        if data.incident_status.order in temp_status_data:
            temp_status_data[data.incident_status.order] += 1
        else:
            temp_status_data[data.incident_status.order] = 1

    for index, each_status in enumerate(incident_status_group):
        if each_status['order'] in temp_status_data:
            incident_status_group[index]['count'] = temp_status_data[each_status['order']]
        else:
            incident_status_group[index]['count'] = 0

    return incident_status_group


def transform_injury_repeater(data):
    new_data = []
    if data:
        for each_injury in data:
            new_data.append(_(each_injury['injury_location']) + " " + _(each_injury['body_part']) + " " + _(each_injury['injury_type']))
        return ",".join(new_data)
    else:
        return ""
