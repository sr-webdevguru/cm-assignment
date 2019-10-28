import base64
import datetime
import json
from django.contrib.auth import get_user_model
from django.db import connection
from django.utils import timezone
from validators.uuid import uuid

from apps.controlled_substance.models import Stock, StockAssignment, USED, OUT
from apps.controlled_substance.utils import add_log, mark_stock_entry_used, \
    unmark_used_stock_entry
from apps.custom_user.utils import validate_email
from apps.incidents.models import Incident
from apps.incidents.models import IncidentNotes, StatusHistory
from apps.incidents.models import IncidentStatus
from apps.incidents.models import IncidentTemplate
from helper_functions import replace_null, create_client

PATIENT_FIELD = ['email', 'phone', 'dob', 'sex', 'name', 'address', 'suburb', 'state', 'country', 'postcode']

special_validation_case = {
    "field_52ca456962ba8": {
        "repeating": False,
        "special": True,
        "fields": {
            "lat": {
                "Type": 'number',
                "Required": True,
                "Values": ''
            },
            "long": {
                "Type": 'number',
                "Required": True,
                "Values": ''
            },
            "accuracy": {
                "Type": 'number',
                "Required": True,
                "Values": ''
            }
        }
    },
    "incident_id": {
        "Type": 'UUID',
        "Required": False,
        "Values": '',
        "repeating": False
    },
    "incident_pk": {
        "Type": 'number',
        "Required": False,
        "Values": '',
        "repeating": False
    },
    "dt_created": {
        "Type": 'date_time_picker',
        "Required": False,
        "Values": '',
        "repeating": False
    },
    "incident_status": {
        "repeating": False,
        "special": True,
        "fields": {
            "incident_status_id": {
                "Type": 'number',
                "Required": False,
                "Values": [1, 2, 3, 4, 5, 6, 7, 8, 9]
            }
        }
    },
    "assigned_to": {
        "Type": 'UUID',
        "Required": False,
        "Values": '',
        "repeating": False
    },
    "reporter_name": {
        "Type": 'text',
        "Required": False,
        "Values": '',
        "repeating": False
    },
    "reporter_phone": {
        "Type": 'text',
        "Required": False,
        "Values": '',
        "repeating": False
    },
    "controlled_substance_stock_assignment_id": {
        "Type": 'UUID',
        "Required": False,
        "Values": '',
        "repeating": False
    },
    "drug_administered_by": {
        "Type": 'UUID',
        "Required": False,
        "Values": '',
        "repeating": False
    }
}

NOTES_FIELD_ADDITION = {
    "note_id": {
        "Type": 'number',
        "Required": False,
        "Values": '',
        "repeating": False
    }
}

MEDIA_FIELD = ['media_reference', 'media_type']

TEMPORARY_EXCLUDED_FIELDS = ['blood_pressure_diastolic',
                             'blood_pressure_systolic',
                             'dose_administered',
                             'heart_rate',
                             'pain_score',
                             'patient_age',
                             'respiration_rate',
                             'field_52d4798f6d229']

TEMPORARY_SANITIZE_FIELD = ['field_52ca447762ba2', 'incident_role']

def get_template():
    template = IncidentTemplate.objects.get(pk=1)
    return template.json


def audit_incident(incident, resort, assigned, current_assigned, changed, incident_json):
    cursor = connection.cursor()

    cursor.execute("""INSERT INTO incidents_incidentaudit (
      incident_id,
      resort_id,
      assigned_to_id,
      prev_assigned_to_id,
      changed_by_id,
      incident_data,
      dt_created
    ) VALUES (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        now()
    )
    """, [incident.incident_pk, resort.resort_pk, assigned.user_pk, current_assigned.user_pk, changed.user_pk, json.dumps(incident_json)])
    cursor.close()

    return True


def incident_note(incident_json, user, incident):
    notes = incident_json.get('notes', [])

    incident_notes = list(IncidentNotes.objects.filter(incident=incident).values_list('note_id', flat=True))

    if notes and notes is not None and incident_json:
        for note in notes:
            if note:
                if note.get('note_id') is None:
                    try:
                        note_date = datetime.datetime.strptime(note.get('field_52ca448dg94ja4'), "%Y-%m-%d %H:%M:%S")
                    except:
                        note_date = datetime.datetime.now()

                    try:
                        user = get_user_model().objects.get(user_id=note.get('field_52ca448dg94ja5'))
                    except:
                        user = user

                    new_note = IncidentNotes(incident=incident, note=note.get('field_52ca448dg94ja3'),
                                             note_date=note_date, user=user)
                    new_note.save()
                    note['note_id'] = new_note.note_id
                else:
                    try:
                        incident_notes.remove(note.get('note_id'))
                    except:
                        pass

                    note_data = IncidentNotes.objects.get(note_id=note.get('note_id'))

                    note_data.note = note.get('field_52ca448dg94ja3')
                    note_data.note_date = datetime.datetime.strptime(note.get('field_52ca448dg94ja4'),
                                                                     "%Y-%m-%d %H:%M:%S")
                    note_data.save()

        IncidentNotes.objects.filter(pk__in=incident_notes).delete()

    return notes


def status_history(incident, status, user, date=None):
    if date is None:
        date = timezone.now()

    new_status = StatusHistory(incident=incident, status=status, user=user, status_date=date)
    new_status.save()

    return new_status


def incident_status_option(selected_status):
    incident_status = IncidentStatus.objects.all()
    options = []

    for status in incident_status:
        a = dict()
        if status.order == selected_status:
            a['key'] = status.key
            a['value'] = status.order
            a['color'] = status.color
            options.append(a)

    return options


def incident_status_option_for_status_report(selected_status):
    incident_status = IncidentStatus.objects.all()

    status_resp = dict()
    for status in incident_status:
        if status.order == selected_status:
            status_resp['status_label'] = status.key
            status_resp['status_id'] = status.order

    return status_resp


def get_extra_incident_info(config, incident_json, incident_pk, purpose, data_key):
    data = {}

    try:
        injuries_json = config['DashboardItems']['field_52d4798f6d229']['Questions']['field_52d4798f6d227'][
            'RepeatingQuestions']
        patient_history_json = config['DashboardItems']['field_52ca41790a16c']['Questions']
        treatment_info = config['DashboardItems']['field_52ca42230a171']['Questions']

        injury_location_values = injuries_json['injury_location']['Values']
        body_part_values = injuries_json['body_part']['Values']
        injury_type_values = injuries_json['injury_type']['Values']
        activity_values = patient_history_json['field_52ca3dc8ac437']['Values']
        treatments = treatment_info['field_52ca445d62ba1']['Values']

    except:
        pass

    if purpose == 'list':
        try:
            location = incident_json['field_52ca456962ba8']
            data['location'] = location
        except:
            data['location'] = {"lat": "",
                                "long": "",
                                "accuracy": ""}

        try:
            photos = incident_json['field_52d47a654d1aa']
            photo_list = []
            for photo in photos:
                photo_list.append(photo['photo'])
            data['images'] = photo_list
        except:
            data['images'] = []

        try:
            treatment_given = []
            treatment_detail = incident_json['field_52ca445d62ba1']
            for treatment in treatment_detail:
                for treatment_val in treatments:
                    if treatment_val.keys()[0] == treatment:
                        treatment_given.append({treatment: treatment_val[treatment]})
            data['treatment'] = treatment_given
        except:
            data['treatment'] = []

    patient = get_patient_info(incident_pk, data_key)

    data['patient'] = {
        'name': patient['name'],
        'phone': patient['phone'],
        'sex': patient['sex']
    }

    injury_data = []
    try:
        injury_info = incident_json['field_52d4798f6d227']
        for index, injury in enumerate(injury_info):
            temp_injury_data = {}
            try:
                injury_location_key = injury['injury_location']
                for injury_location in injury_location_values:
                    if injury_location.keys()[0] == injury_location_key:
                        temp_injury_data.update({'injury_location': injury_location[injury_location_key]})
            except:
                temp_injury_data.update({'injury_location': ""})

            try:
                body_part_key = injury['body_part']
                for body_part in body_part_values:
                    if body_part.keys()[0] == body_part_key:
                        temp_injury_data.update({'body_part': body_part[body_part_key]})
            except:
                temp_injury_data.update({'body_part': ""})

            try:
                injury_type_key = injury['injury_type']
                for injury_type in injury_type_values:
                    if injury_type.keys()[0] == injury_type_key:
                        temp_injury_data.update({'injury_type': injury_type[injury_type_key]})
            except:
                temp_injury_data.update({'injury_type': ""})

            injury_data.append(temp_injury_data)

        if not injury_data:
            raise Exception

    except:
        injury_data.append({
            "body_part": "",
            "injury_location": "",
            "injury_type": ""
        })

    try:
        activity_key = incident_json['field_52ca3dc8ac437']
        for activity in activity_values:
            if activity.keys()[0] == activity_key:
                data['activity'] = activity[activity_key]
    except:
        data['activity'] = ""

    data['injury'] = injury_data

    return replace_null(data)


def get_extra_incident_info_status_report(config, incident_json):
    try:
        injuries_json = config['DashboardItems']['field_52d4798f6d229']['Questions']['field_52d4798f6d227'][
            'RepeatingQuestions']
        injury_location_values = injuries_json['injury_location']['Values']
        body_part_values = injuries_json['body_part']['Values']
        injury_type_values = injuries_json['injury_type']['Values']

        area_name_values = config['DashboardItems']['field_52ca41c50a16f']['Questions']['field_554f7cbb3d784']['Values']

        run_name_field = None
        for field, value in incident_json.iteritems():
            if field.startswith('field_551c8bbb3d785_'):
                run_name_values = config['DashboardItems']['field_52ca41c50a16f']['Questions'][field]['Values']
                run_name_field = field

        referred_to_values = config['DashboardItems']['field_52ca42770a179']['Questions']['field_52d48077a16be']['Values']
    except:
        pass

    response_data = {}

    # get injury information
    injury_data = []
    try:
        injury_info = incident_json['field_52d4798f6d227']
        for index, injury in enumerate(injury_info):
            temp_injury_data = {}
            try:
                injury_location_key = injury['injury_location']
                for injury_location in injury_location_values:
                    if injury_location.keys()[0] == injury_location_key:
                        temp_injury_data.update({'injury_location': injury_location[injury_location_key]})
            except:
                temp_injury_data.update({'injury_location': ""})

            try:
                body_part_key = injury['body_part']
                for body_part in body_part_values:
                    if body_part.keys()[0] == body_part_key:
                        temp_injury_data.update({'body_part': body_part[body_part_key]})
            except:
                temp_injury_data.update({'body_part': ""})

            try:
                injury_type_key = injury['injury_type']
                for injury_type in injury_type_values:
                    if injury_type.keys()[0] == injury_type_key:
                        temp_injury_data.update({'injury_type': injury_type[injury_type_key]})
            except:
                temp_injury_data.update({'injury_type': ""})

            injury_data.append(temp_injury_data)

        if not injury_data:
            raise Exception

    except:
        injury_data.append({
            "body_part": "",
            "injury_location": "",
            "injury_type": ""
        })
    response_data.update({"injury": injury_data})

    # get location information
    location = {}
    try:
        area_name_key = incident_json['field_554f7cbb3d784']
        for area in area_name_values:
            if area.keys()[0] == area_name_key:
                location.update({'area_name': area[area_name_key]})
            else:
                location.update({'area_name': ""})
    except:
        location.update({'area_name': ""})

    try:
        run_name_key = incident_json[run_name_field]
        for run in run_name_values:
            if run.keys()[0] == run_name_key:
                location.update({'run_name': run[run_name_key]})
            else:
                location.update({'run_name': ""})
    except:
        location.update({'run_name': ""})
    response_data.update({"location": location})

    # get referred to information
    try:
        referred_to_key = incident_json['field_52d48077a16be']
        for referred_to in referred_to_values:
            if referred_to.keys()[0] == referred_to_key:
                response_data.update({"referred_to": referred_to[referred_to_key]})
            else:
                response_data.update({"referred_to": ""})
    except:
        response_data.update({"referred_to": ""})

    return response_data


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
        ]


# get encypted data key from the data
def get_data_key(resort):
    client = create_client()
    response = client.decrypt(CiphertextBlob=base64.b64decode(resort.enc_data_key))

    return base64.b64encode(response['Plaintext'])


def get_patient_info(incident_pk, data_key):
    cursor = connection.cursor()

    cursor.execute("""SELECT
  pgp_sym_decrypt(name, keys.datakey)     AS name,
  sex,
  pgp_sym_decrypt(address, keys.datakey)  AS address,
  pgp_sym_decrypt(suburb, keys.datakey)   AS suburb,
  pgp_sym_decrypt(state, keys.datakey)    AS state,
  pgp_sym_decrypt(postcode, keys.datakey) AS postcode,
  country,
  pgp_sym_decrypt(phone, keys.datakey)    AS phone,
  pgp_sym_decrypt(email, keys.datakey)    AS email,
  pgp_sym_decrypt(dob, keys.datakey) AS dob
FROM incidents_patients
CROSS JOIN (SELECT %s::TEXT As datakey) As keys
WHERE incidents_patients.incident_id = %s;""", [data_key, incident_pk])

    data = dictfetchall(cursor)
    cursor.close()

    return replace_null(data[0])


def merge_patient_data_for_update(incident_pk, incident_data, new_incident, data_key):
    patient_data_available = False
    patient_data = None

    incident_data_patient_field = {
        'email': incident_data.get('email'),
        'phone': incident_data.get('phone'),
        'dob': incident_data.get('dob'),
        'sex': incident_data.get('sex'),
        'name': incident_data.get('name'),
        'address': incident_data.get('address'),
        'suburb': incident_data.get('suburb'),
        'state': incident_data.get('state'),
        'country': incident_data.get('country'),
        'postcode': incident_data.get('postcode')
    }

    if new_incident:
        patient_data = incident_data_patient_field
    else:
        for field in PATIENT_FIELD:
            if field in incident_data:
                patient_data_available = True
                break
        if patient_data_available:
            patient_data = get_patient_info(incident_pk, data_key)
            patient_data.update({k: v for k, v in incident_data_patient_field.iteritems() if v is not None})

    incident_data.pop('email', None)
    incident_data.pop('phone', None)
    incident_data.pop('dob', None)
    incident_data.pop('sex', None)
    incident_data.pop('name', None)
    incident_data.pop('address', None)
    incident_data.pop('suburb', None)
    incident_data.pop('state', None)
    incident_data.pop('country', None)
    incident_data.pop('postcode', None)

    return patient_data, incident_data


def update_patient(incident_json, incident_pk, created, data_key):
    cursor = connection.cursor()

    if created:

        patient_data, incident_data = merge_patient_data_for_update(incident_pk, incident_json, True, data_key)

        cursor.execute("""INSERT INTO incidents_patients (
                        patient_id,
                        incident_id,
                        name,
                     sex,
                     address,
                     suburb,
                     state,
                     postcode,
                     country,
                     phone,
                     email,
                     dob
                    )
                    SELECT
                     v.patient_id,
                     v.incident_id,
                     pgp_sym_encrypt(v.name, keys.datakey, 'compress-algo=1, cipher-algo=aes256') As name,
                     v.sex,
                     pgp_sym_encrypt(v.address, keys.datakey, 'compress-algo=1, cipher-algo=aes256') As address,
                     pgp_sym_encrypt(v.suburb, keys.datakey, 'compress-algo=1, cipher-algo=aes256') As suburb,
                     pgp_sym_encrypt(v.state,keys.datakey, 'compress-algo=1, cipher-algo=aes256') As state,
                     pgp_sym_encrypt(v.postcode, keys.datakey, 'compress-algo=1, cipher-algo=aes256') As postcode,
                     v.country,
                     pgp_sym_encrypt(v.phone,keys.datakey, 'compress-algo=1, cipher-algo=aes256') As phone,
                     pgp_sym_encrypt(v.email, keys.datakey, 'compress-algo=1, cipher-algo=aes256') As email,
                      pgp_sym_encrypt(v.dob, keys.datakey, 'compress-algo=1, cipher-algo=aes256') As dob
                    FROM (
                      VALUES (
                       uuid_generate_v4(),
                       %s,
                       %s,
                       %s,
                       %s,
                       %s,
                       %s,
                       %s,
                       %s,
                       %s,
                       %s,
                       %s
                      )
                        ) AS v (
                       patient_id,
                       incident_id,
                       name,
                       sex,
                       address,
                       suburb,
                       state,
                       postcode,
                       country,
                       phone,
                       email,
                       dob
                      )
CROSS JOIN (SELECT %s::TEXT As datakey) As keys;""", [incident_pk, patient_data['name'], patient_data['sex'], patient_data['address'], patient_data['suburb'],
                patient_data['state'], patient_data['postcode'], patient_data['country'], patient_data['phone'],
                patient_data['email'], patient_data['dob'], data_key])

    else:
        patient_data, incident_data = merge_patient_data_for_update(incident_pk, incident_json, False, data_key)

        if patient_data is not None:
            cursor.execute("""UPDATE incidents_patients SET
                            name = pgp_sym_encrypt(v.name, keys.datakey, 'compress-algo=1, cipher-algo=aes256'),
                         sex = v.sex,
                         address = pgp_sym_encrypt(v.address, keys.datakey, 'compress-algo=1, cipher-algo=aes256'),
                         suburb = pgp_sym_encrypt(v.suburb, keys.datakey, 'compress-algo=1, cipher-algo=aes256'),
                         state = pgp_sym_encrypt(v.state,keys.datakey, 'compress-algo=1, cipher-algo=aes256'),
                         postcode = pgp_sym_encrypt(v.postcode, keys.datakey, 'compress-algo=1, cipher-algo=aes256'),
                         country = v.country,
                         phone = pgp_sym_encrypt(v.phone,keys.datakey, 'compress-algo=1, cipher-algo=aes256'),
                         email = pgp_sym_encrypt(v.email, keys.datakey, 'compress-algo=1, cipher-algo=aes256'),
                         dob = pgp_sym_encrypt(v.dob, keys.datakey, 'compress-algo=1, cipher-algo=aes256')
                        FROM (
                          VALUES (
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s
                          )
                            ) AS v (
                           name,
                           sex,
                           address,
                           suburb,
                           state,
                           postcode,
                           country,
                           phone,
                           email,
                           dob
                          )
CROSS JOIN (SELECT %s::TEXT As datakey) As keys
WHERE incidents_patients.incident_id = %s;""", [patient_data['name'], patient_data['sex'], patient_data['address'],
                                                patient_data['suburb'], patient_data['state'], patient_data['postcode'],
                                                patient_data['country'], patient_data['phone'], patient_data['email'],
                                                patient_data['dob'], data_key, incident_pk])

    cursor.execute("UPDATE incidents_incident SET incident_data = %s WHERE incident_pk = %s",
                   [json.dumps(incident_data), incident_pk])
    cursor.close()

    return incident_data


def get_incident_data(incident_pk):
    cursor = connection.cursor()
    cursor.execute("SELECT incident_data FROM incidents_incident WHERE incident_pk = %s;", [incident_pk])
    data = cursor.fetchone()
    cursor.close()
    if data[0] is None:
        return None
    return replace_null(data[0])


def update_incident_data(incident_pk, json_data):
    cursor = connection.cursor()
    cursor.execute("UPDATE incidents_incident SET incident_data = %s WHERE incident_pk = %s;",
                   [json.dumps(json_data), incident_pk])
    cursor.close()

    return json_data


# Functions for print incident API which merges incident_config with incident_data

# This handles the "Questions"
def handle_question(incident_data, incident_config):
    for question_key, question_val in incident_config.iteritems():
        type = question_val.get('Type', '')
        if type == 'select' or type == 'radio' or type == 'gender' or \
                        type == 'arrows' or type == 'radio_button':
            try:
                question_val['selected'] = {'key': incident_data.get(question_key, ''), 'value':
                    next(d for i, d in enumerate(question_val['Values']) if incident_data.get(question_key, '') in d)[
                        incident_data.get(question_key, '')]}
            except:
                question_val['selected'] = {"key": "", "value": ""}

        elif type == 'multi_select':
            try:
                temp = []
                incident_val = incident_data.get(question_key)
                for index, value in enumerate(incident_val):
                    temp.append(next(d for i, d in enumerate(question_val['Values']) if incident_val[index] in d)[
                                    incident_val[index]])
                question_val['selected'] = temp
            except:
                question_val['selected'] = []

        elif type == 'repeater':
            try:
                question_val['selected'] = handle_repeating_question(incident_data.get(question_key, ''),
                                                                     question_val.get('RepeatingQuestions', ''))
            except:
                question_val['selected'] = []
        else:
            try:
                question_val['selected'] = incident_data.get(question_key, '')
            except:
                question_val['selected'] = ''

    return incident_config


# This handles the "RepeatingQuestions"
def handle_repeating_question(incident_data, incident_config):
    for val in incident_data:
        for key, value in incident_config.iteritems():
            type = value.get('Type', '')
            if type == 'select' or type == 'radio' or type == 'gender' or \
                            type == 'arrows' or type == 'radio_button':
                try:
                    val[key] = {'key': val.get(key, ''),
                                'value': next(d for i, d in enumerate(value['Values']) if val.get(key, '') in d)[
                                    val.get(key, '')]}
                except:
                    val[key] = {"key": "", "value": ""}
            else:
                try:
                    val[key] = val.get(key, '')
                except:
                    val[key] = ''

    return incident_data


def merge_incident(incident_json, resort):
    main_json = resort.incident_template['DashboardItems']
    for incident_key, incident_val in main_json.iteritems():
        if incident_val.has_key("Questions"):
            incident_val['Questions'] = handle_question(incident_json, incident_val.get('Questions', ''))
        elif incident_val.has_key("RepeatingQuestions"):
            incident_val['selected'] = handle_repeating_question(incident_json.get(incident_key, ''),
                                                                 incident_val.get('RepeatingQuestions', ''))
    return main_json


def get_full_incident(incident_pk):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM incidents_incident WHERE incident_pk = %s;", [incident_pk])
    data = dictfetchall(cursor)
    cursor.close()

    return data[0]

def clean_data(resort, data):
    template = resort.incident_template['DashboardItems']
    keys = ['address', 'assigned_to', 'country', 'dob', 'dt_created', 'email', 'incident_id', 'incident_pk',
            'incident_status', 'name', 'phone', 'postcode', 'sex', 'state', 'suburb']
    for key, value in template.iteritems():
        keys.append(key)
        if 'Questions' in value:
            for kKey, vValue in value['Questions'].iteritems():
                keys.append(kKey)
                if 'Questions' in vValue:
                    for kkKey, vvValue in vValue['Questions'].iteritems():
                        keys.append(kkKey)
                elif 'RepeatingQuestions' in vValue:
                    for kkKey, vvValue in vValue['RepeatingQuestions'].iteritems():
                        keys.append(kkKey)
        elif 'RepeatingQuestions' in value:
            for kKey, vValue in value['RepeatingQuestions'].iteritems():
                keys.append(kKey)
                if 'Questions' in vValue:
                    for kkKey, vvValue in vValue['Questions'].iteritems():
                        keys.append(kkKey)
                elif 'RepeatingQuestions' in vValue:
                    for kkKey, vvValue in vValue['RepeatingQuestions'].iteritems():
                        keys.append(kkKey)
    newData = {}
    for key, value in data.iteritems():
        if key in keys:
            newData[key] = value
    return newData

def merge_incident_data(incident_data, update_data):
    if incident_data is not None:
        for k, v in update_data.iteritems():
            if (k in incident_data and isinstance(incident_data[k], dict) and isinstance(update_data[k], dict)):
                merge_incident_data(incident_data[k], update_data[k])
            else:
                incident_data[k] = update_data[k]
    else:
        return update_data
    return incident_data


def get_incident_sequence(resort):
    today_datetime = datetime.date.today()
    if today_datetime.month < resort.season_start_date.month:
        startDate = datetime.date(today_datetime.year - 1, resort.season_start_date.month, resort.season_start_date.day)
    elif today_datetime.month == resort.season_start_date.month:
        if today_datetime.day < resort.season_start_date.day:
            startDate = datetime.date(today_datetime.year - 1, resort.season_start_date.month,
                                      resort.season_start_date.day)
        else:
            startDate = datetime.date(today_datetime.year, resort.season_start_date.month, resort.season_start_date.day)
    else:
        startDate = datetime.date(today_datetime.year, resort.season_start_date.month, resort.season_start_date.day)
    endDate = startDate + datetime.timedelta(days=365)
    # Backup of original filtering used for incident filtering
    # incident_count = Incident.objects.filter(dt_created__gte=startDate, dt_created__lte=endDate, resort=resort).latest('dt_modified')
    try:
        last_incident = Incident.objects.filter(dt_created__gte=startDate, dt_created__lte=endDate,
                                                resort=resort).exclude(incident_status__order=9).latest(
            'incident_sequence')
        return last_incident.incident_sequence + 1
    except:
        return 1


def process_values_for_drug_administered(values):
    final_list = []
    for each_value in values:
        try:
            int(each_value.keys()[0])
            final_list.append(each_value.keys()[0])
        except:
            int(each_value.keys()[1])
            final_list.append(each_value.keys()[1])

    return final_list


# Incoming incident data validation
def create_or_retrieve_validation_conditions(resort):
    incident_template_merged = {}
    for each_key, each_value in resort.incident_template['DashboardItems'].iteritems():
        if each_value.has_key('Questions'):
            for key, value in each_value['Questions'].iteritems():
                if value.has_key('RepeatingQuestions'):
                    temp_dict = {}
                    for key2, value2 in value['RepeatingQuestions'].iteritems():
                        if key2 == 'drug_administered':
                            temp_dict.update({key2: {"Type": value2['Type'], "Required": value2['Required'],
                                                     "Values": process_values_for_drug_administered(value2['Values']) if
                                                     value2['Values'] else "", "repeating": False}})
                        else:
                            temp_dict.update({key2: {"Type": value2['Type'], "Required": value2['Required'],
                                                     "Values": [c.keys()[0] for c in value2['Values']] if value2[
                                                         'Values'] else "", "repeating": False}})
                            if each_key == 'notes':
                                temp_dict.update(NOTES_FIELD_ADDITION)
                    incident_template_merged.update({key: {"fields": temp_dict, "repeating": True}})
                else:
                    incident_template_merged.update({key: {"Type": value['Type'], "Required": value['Required'],
                                                           "Values": [c.keys()[0] for c in value['Values']],
                                                           "repeating": False}})
        elif each_value.has_key('RepeatingQuestions'):
            temp_dict = {}
            for key1, value1 in each_value['RepeatingQuestions'].iteritems():
                temp_dict.update({key1: {"Type": value1['Type'], "Required": value1['Required'],
                                         "Values": [c.keys()[0] for c in value1['Values']] if value1['Values'] else "",
                                         "repeating": False}})
            if each_key == 'notes':
                temp_dict.update(NOTES_FIELD_ADDITION)
            incident_template_merged.update({each_key: {"fields": temp_dict, "repeating": True}})

    # Merge two dictionary
    z = incident_template_merged.copy()
    z.update(special_validation_case)
    return z


MISSING_FIELD = 0
INVALID_DATA = 1
KEY_NOT_FOUND = 2
CUSTOM_MESSAGE = 3


def validation_message(message_type, key, value_type=None, custom_message=None):
    message = {}
    if message_type == MISSING_FIELD:
        message = {key: "field is missing"}
    elif message_type == INVALID_DATA:
        message = {key: "must be %s" % value_type}
    elif message_type == KEY_NOT_FOUND:
        message = {key: "key not found"}
    elif message_type == CUSTOM_MESSAGE:
        message = {key: custom_message}
    return message


def field_data_validation_correction(data, field_type, values, key):
    if field_type in ['arrows', 'radio', 'select', 'gender', 'radio_button']:
        if (isinstance(data, str) or isinstance(data, unicode)) and data:
            if not (data in values):
                if data.lower() in values:
                    return True, "", data.lower()
                else:
                    return False, validation_message(INVALID_DATA, key,
                                                     "one of the " + ','.join(map(str, values))), data
            else:
                return True, "", data
        elif (data is None) or (not data):
            return True, "", ""
        else:
            return False, validation_message(INVALID_DATA, key, 'string'), data

    elif field_type in ['height', 'weight', 'range', 'distance', 'length', 'altitude', 'decimal', 'temperature']:
        if not (isinstance(data, int) or isinstance(data, float)):
            try:
                if data is None:
                    return True, "", None
                else:
                    return True, "", float(data)
            except:
                return False, validation_message(INVALID_DATA, key, "integer or float"), data
        else:
            return True, "", data

    # elif field_type in []:
    #     if not isinstance(data, int):
    #         return validation_message(INVALID_DATA, key, "integer")

    # elif field_type in []:
    #     if isinstance(data, float):
    #         if not (len(str(data).rsplit('.')[-1]) == 1):
    #             return validation_message(INVALID_DATA, key, "single decimal place")
    #     elif isinstance(data, int):
    #         pass
    #     else:
    #         return validation_message(INVALID_DATA, key, "float")

    elif field_type in ['patient_age', 'number']:
        if not isinstance(data, int):
            try:
                if data is None:
                    return True, "", None
                else:
                    return True, "", int(data)
            except:
                return False, validation_message(INVALID_DATA, key, "int"), data
        else:
            return True, "", data

    elif field_type in ['UUID']:
        if not uuid(data):
            return False, validation_message(INVALID_DATA, key, "UUID"), data
        else:
            return True, "", data

    elif field_type in ['date_picker']:
        try:
            if data and data != "-1":
                datetime_data = data[:10]
                datetime.datetime.strptime(datetime_data, '%Y-%m-%d')
                return True, "", datetime_data
            else:
                return True, "", ""
        except:
            return False, validation_message(INVALID_DATA, key, 'of the format YYYY-MM-DD'), data

    elif field_type in ['date_time_picker']:
        try:
            if data and data != "-1":
                datetime_data = data[:19]
                datetime.datetime.strptime(datetime_data, '%Y-%m-%d %H:%M:%S')
                return True, "", datetime_data
            else:
                return True, "", ""
        except:
            return False, validation_message(INVALID_DATA, key, 'of the format YYYY-MM-DD HH:MM:SS'), data

    elif field_type in ['file', 'image', 'message', 'signature', 'text', 'textarea']:
        if not (isinstance(data, str) or isinstance(data, unicode)):
            if data is None:
                return True, "", ""
            else:
                return False, validation_message(INVALID_DATA, key, 'string'), data
        else:
            return True, "", data

    elif field_type in ['email']:
        try:
            if (data is None) or (not data):
                return True, "", ""
            else:
                email_name, domain_part = data.strip().rsplit('@', 1)
                email = '@'.join([email_name.lower(), domain_part.lower()])
                if not validate_email(email):
                    return False, validation_message(INVALID_DATA, key, 'email format'), data
                else:
                    return True, "", email
        except:
            return False, validation_message(INVALID_DATA, key, 'valid email format'), data

    elif field_type in ['multi_select']:
        missing_values = []

        try:
            if data:
                for data_id, each_value in enumerate(data):
                    if type(each_value) == str:
                        pass
                    else:
                        data[data_id] = str(each_value)
            elif (data == "") or (data is None) or (data == {}):
                return True, "", []
        except:
            if key in TEMPORARY_SANITIZE_FIELD:
                return True, "", []
            else:
                return False, validation_message(INVALID_DATA, key, 'array of string'), data

        for value in data:
            if (not (value in values)) and value:
                missing_values.append(value)
        if missing_values:
            return False, validation_message(CUSTOM_MESSAGE, key, custom_message='%s is not valid choice' % ','.join(
                map(str, missing_values))), data
        else:
            return True, "", data
    elif field_type in ['hidden']:
        return True, "", data
    else:
        return False, validation_message(CUSTOM_MESSAGE, key, custom_message='%s type not found' % field_type), data


def incident_data_correction_validation(incoming_data, validation_conditions):
    """
    corrects where possible and validates incoming incident data
    :param incoming_data: incoming incident data
    :param validation_conditions: validation conditions to check
    :type incoming_data: dict
    :type validation_conditions: dict
    :return: corrected_data incoming incident data after correction
    """
    corrected_data = incoming_data
    validation_error = {}
    missing_fields = []
    missing_fields_with_data = []

    for key, value in corrected_data.iteritems():
        if validation_conditions.has_key(key):

            # special case of validation and correction for location and incident status
            if validation_conditions[key].has_key('special'):
                fields = validation_conditions[key]['fields']

                # Location data validation and correction
                if key == 'field_52ca456962ba8':
                    for k, v in value.iteritems():
                        if fields.has_key(k):
                            try:
                                if v is not None and v:
                                    value[k] = float(v)
                                elif not v:
                                    value[k] = None
                            except:
                                validation_error.update(validation_message(INVALID_DATA, k, 'integer (or) float'))
                        else:
                            validation_error.update(
                                validation_message(CUSTOM_MESSAGE, k, custom_message='not found in location'))

                # Incident status data validation and correction
                elif key == 'incident_status':
                    try:
                        incident_status_id = int(value['incident_status_id'])
                        if not (incident_status_id in fields['incident_status_id']['Values']):
                            validation_error.update(
                                validation_message(INVALID_DATA, 'incident_status_id', 'between 1 and 9'))
                        else:
                            value['incident_status_id'] = incident_status_id
                    except KeyError:
                        validation_error.update(validation_message(MISSING_FIELD, 'incident_status_id'))
                    except ValueError:
                        validation_error.update(validation_message(INVALID_DATA, 'incident_status_id', 'integer'))

            # validation for non-repeating field
            elif not validation_conditions[key]['repeating']:
                valid, message, final_value = field_data_validation_correction(value,
                                                                               validation_conditions[key]['Type'],
                                                                               validation_conditions[key]['Values'],
                                                                               key)
                # if its not valid value then pass on the validation message
                if not valid:
                    validation_error.update(message)
                # if its valid value then update its value to the final_data which is cleaned version of original data
                else:
                    corrected_data[key] = final_value

            # validation for repeating field
            elif validation_conditions[key]['repeating']:

                if type(value) == list:
                    for idx, each_value in enumerate(value):
                        if each_value and (each_value is not None):
                            try:
                                for key2, value2 in each_value.iteritems():

                                    # special media field validation
                                    if key2 in MEDIA_FIELD:
                                        if value2:
                                            if not (isinstance(value2, str) or isinstance(value2, unicode)):
                                                validation_error.update(validation_message(INVALID_DATA, key, 'string'))
                                        elif (not value2) or (value2 is None):
                                            corrected_data[key][idx][key2] = ""
                                    elif key2 in special_validation_case:
                                        valid, message, final_value = field_data_validation_correction(value2,
                                                                                                       special_validation_case[key2]['Type'],
                                                                                                       special_validation_case[key2]['Values'],
                                                                                                       key2
                                                                                                       )
                                        if not valid:
                                            validation_error.update(message)
                                        else:
                                            corrected_data[key][idx][key2] = final_value
                                    elif key2.startswith('drug_administered_by_'):
                                        valid, message, final_value = field_data_validation_correction(value2,
                                                                                                       special_validation_case['drug_administered_by']['Type'],
                                                                                                       special_validation_case['drug_administered_by']['Values'],
                                                                                                       key2
                                                                                                       )
                                        if not valid:
                                            validation_error.update(message)
                                        else:
                                            corrected_data[key][idx][key2] = final_value
                                    elif key in validation_conditions and key2 in validation_conditions[key]['fields']:
                                        valid, message, final_value = field_data_validation_correction(value2,
                                                                                                       validation_conditions[key]['fields'][key2]['Type'],
                                                                                                       validation_conditions[key]['fields'][key2]['Values'],
                                                                                                       key2
                                                                                                       )
                                        # if its not valid value then pass on the validation message
                                        if not valid:
                                            validation_error.update(message)
                                        # if its valid value then update its value to the final_data which is cleaned version of original data
                                        else:
                                            corrected_data[key][idx][key2] = final_value
                            except AttributeError:
                                validation_error.update(validation_message(INVALID_DATA, key, 'set of dictionary'))
                        else:
                            corrected_data[key][idx] = {}

                elif (not value) or (value is None):
                    corrected_data[key] = []
                else:
                    validation_error.update(validation_message(INVALID_DATA, key, 'array'))
        else:
            if key not in TEMPORARY_EXCLUDED_FIELDS:
                missing_fields.append(key)
                missing_fields_with_data.append({key: value})

    if missing_fields:
        for val in missing_fields:
            corrected_data.pop(val, None)

    return corrected_data, validation_error, missing_fields_with_data


def validate_incident_data(incoming_data, resort):
    validation_conditions = create_or_retrieve_validation_conditions(resort)
    incoming_data, validation_error, missing_fields_with_data = incident_data_correction_validation(incoming_data,
                                                                                                    validation_conditions)

    return incoming_data, validation_error, missing_fields_with_data


def check_drug_administered(incoming_data, incident, user):
    updated_drug_administered = []

    if 'field_52d4800164f2e' in incoming_data:
        for id, value in enumerate(incoming_data['field_52d4800164f2e']):
            extra_data = {}
            if not ('controlled_substance_stock_assignment_id' in value):
                for key, val in value.iteritems():
                    if key.startswith('drug_administered_by_'):
                        stock = Stock.objects.get(controlled_substance_stock_id=val)
                        stock_assignment = StockAssignment.objects.get(controlled_substance_stock=stock)

                        if stock.current_status != USED:
                            stock.current_status = USED
                            stock.save()
                            stock_assignment.controlled_substance_stock_assignment_status = USED
                            stock_assignment.incident_id = incident
                            stock_assignment.dt_used = timezone.now()
                            stock_assignment.save()

                            status, message = mark_stock_entry_used(incident.resort, stock)

                            # create log entry
                            log_entry = 'Item %s : %s %s of %s was used by %s on incident %s' % (str(stock.controlled_substance_stock_pk),
                                                                                                 str(stock.volume),
                                                                                                 stock.controlled_substance.units,
                                                                                                 stock.controlled_substance.controlled_substance_name,
                                                                                                 stock_assignment.user.name,
                                                                                                 str(incident.incident_sequence) if incident.resort.use_sequential_incident_id else str(incident.incident_pk))
                            add_log(log_entry=log_entry, resort=incident.resort, user=user)
                        else:
                            log_entry = 'Tried to allocate item %d : %d  %s of %s to %s on incident %d but item already used.' % (
                                stock.controlled_substance_stock_pk, stock.volume, stock.controlled_substance.units,
                                stock.controlled_substance.controlled_substance_name, user.name,
                                incident.incident_sequence if incident.resort.use_sequential_incident_id else incident.incident_pk)
                            add_log(log_entry=log_entry, resort=incident.resort, user=user)
                            continue

                        extra_data = {'controlled_substance_stock_assignment_id': str(
                            stock_assignment.controlled_substance_stock_assignment_id)}
                if extra_data:
                    value.update(extra_data)
                    updated_drug_administered.append(value)
            elif 'controlled_substance_stock_assignment_id' in value:
                stock_assignment = StockAssignment.objects.get(controlled_substance_stock_assignment_id=value['controlled_substance_stock_assignment_id'])

                if str(stock_assignment.controlled_substance_stock.controlled_substance_stock_id) != value['drug_administered_by_'+ value['drug_administered']]:

                    new_stock = Stock.objects.get(controlled_substance_stock_id=value['drug_administered_by_'+ value['drug_administered']])
                    new_stock_assignment = StockAssignment.objects.get(controlled_substance_stock=new_stock)

                    if new_stock.current_status != USED:
                        new_stock.current_status = USED
                        new_stock.save()
                        new_stock_assignment.controlled_substance_stock_assignment_status = USED
                        new_stock_assignment.incident_id = incident
                        new_stock_assignment.dt_used = timezone.now()
                        new_stock_assignment.save()

                        status, message = mark_stock_entry_used(incident.resort, new_stock)

                        # create log entry
                        log_entry = 'Item %s : %s %s of %s was used by %s on incident %s' % (str(new_stock.controlled_substance_stock_pk),
                                                                                                 str(new_stock.volume),
                                                                                                 new_stock.controlled_substance.units,
                                                                                                 new_stock.controlled_substance.controlled_substance_name,
                                                                                                 new_stock_assignment.user.name,
                                                                                                 str(incident.incident_sequence) if incident.resort.use_sequential_incident_id else str(incident.incident_pk))
                        add_log(log_entry=log_entry, resort=incident.resort, user=user)
                    else:
                        incident_data = get_incident_data(incident.incident_pk)

                        for id1, value1 in enumerate(incident_data['field_52d4800164f2e']):
                            for key1, val1 in value1.iteritems():
                                if (key1 == "controlled_substance_stock_assignment_id") and (str(value1[key1]) == value['controlled_substance_stock_assignment_id']):
                                    updated_drug_administered.append(value1)

                        log_entry = 'Tried to allocate item %d : %d  %s of %s to %s on incident %d but item already used.' % (
                            new_stock.controlled_substance_stock_pk, new_stock.volume, new_stock.controlled_substance.units,
                            new_stock.controlled_substance.controlled_substance_name, user.name,
                            incident.incident_sequence if incident.resort.use_sequential_incident_id else incident.incident_pk)
                        add_log(log_entry=log_entry, resort=incident.resort, user=user)

                        continue

                    stock = stock_assignment.controlled_substance_stock
                    stock.current_status = OUT
                    stock.save()
                    log_entry = "Item %s : %s %s of %s assigned to %s was removed from incident %s by %s" % (str(stock.controlled_substance_stock_pk),
                                                                                                             str(stock.volume),
                                                                                                             stock.controlled_substance.units,
                                                                                                             stock.controlled_substance.controlled_substance_name,
                                                                                                             stock_assignment.user.name,
                                                                                                             str(incident.incident_sequence) if incident.resort.use_sequential_incident_id else str(incident.incident_pk),
                                                                                                             user.name)

                    add_log(log_entry=log_entry, resort=incident.resort, user=user)
                    stock_assignment.controlled_substance_stock_assignment_status = OUT
                    stock_assignment.incident_id = None
                    stock_assignment.dt_used = None
                    stock_assignment.save()

                    unmark_used_stock_entry(incident.resort, stock)

                    extra_data = {'controlled_substance_stock_assignment_id': str(
                        new_stock_assignment.controlled_substance_stock_assignment_id)}
                    if extra_data:
                        value.update(extra_data)
                        updated_drug_administered.append(value)
                else:
                    updated_drug_administered.append(value)

    if updated_drug_administered:
        incoming_data['field_52d4800164f2e'] = updated_drug_administered
    return incoming_data


# For encrypting and decrypting data
# class AESCipher(object):
#
#     def __init__(self, key, enc_key=None):
#         self.bs = 16
#         self.key = key
#         self.enc_key = enc_key
#
#     def encrypt(self, raw):
#         raw = self._pad(raw)
#         iv = Random.new().read(AES.block_size)
#         cipher = AES.new(self.key, AES.MODE_CBC, iv)
#         return base64.b64encode(iv + cipher.encrypt(raw) + "*-*-*" + self.enc_key)
#
#     def decrypt(self, enc):
#         enc = base64.b64decode(enc)
#         iv = enc[:AES.block_size]
#         enc_key = enc[AES.block_size:].split("*-*-*")[1]
#         cipher = AES.new(self.key, AES.MODE_CBC, iv)
#         return self._unpad(cipher.decrypt(enc[AES.block_size:].split("*-*-*")[0])).decode('utf-8'), enc_key
#
#     def _pad(self, s):
#         return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)
#
#     @staticmethod
#     def _unpad(s):
#         return s[:-ord(s[len(s)-1:])]
