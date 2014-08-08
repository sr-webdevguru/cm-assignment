import json
import re

import urllib3
from django.contrib.auth import get_user_model
from django.core.signing import b64_encode
from rest_framework.authtoken.models import Token

from apps.custom_user.models import UserRoles
from apps.custom_user.serializers import UserSerializer
from apps.devices.models import Devices
from apps.devices.serializers import DeviceSerializer
from apps.resorts.models import UserResortMap
from apps.resorts.serializers import ResortSerializer

user = get_user_model()
pattern = re.compile("^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Za-z]{2,}$")


def get_user_by_email(email):
    return user.objects.filter(email=email).first()


def get_token(user):
    token = Token.objects.filter(user=user).first()

    if token is not None:
        return token.key
    else:
        return None


def user_has_permission(user, resort, role_id):
    try:
        resort_user = UserResortMap.objects.filter(user=user, resort=resort).first()
        if resort_user.role.role_id == role_id:
            return True
        else:
            return False
    except:
        return False


def get_user_resort_combo(user_id, resort_required_data,
                          user_required_data=('user_id', 'name', 'phone', 'email', 'user_connected',
                                              'user_controlled_substances', 'user_asset_management')):
    user_resort = {}
    actual_user = user.objects.get(pk=user_id)

    user_data = UserSerializer(actual_user, fields=user_required_data)
    user_resort = user_data.data

    resorts_user = UserResortMap.objects.filter(user=actual_user)

    resorts = []
    for resort in resorts_user:
        resorts.append(resort.resort)

    resort_data = ResortSerializer(resorts, fields=resort_required_data, many=True)

    user_resort["resorts"] = resort_data.data
    user_resort["role_id"] = userrole_option(resorts_user[len(resorts) - 1].role.role_id) if len(resorts) > 0 else ""
    user_resort["resort_count"] = len(resorts)

    return user_resort


def get_user_resort_status(user, resort):
    from apps.resorts.utils import get_user_resort_map
    user_resort_map = get_user_resort_map(user, resort)
    return user_resort_map.user_status


def get_devices_user(user):
    devices = Devices.objects.filter(device_user=user, device_state=0)

    if devices:
        return DeviceSerializer(devices, fields=('device_id', 'device_type', 'device_os'), many=True).data
    else:
        return []


def userrole_option(selected_role):
    roles = UserRoles.objects.all()
    options = []

    for role in roles:
        a = dict()

        if role.order == selected_role:
            a['key'] = role.key
            a['value'] = role.order
            options.append(a)

    return options


def inject_patroller(resort, user, operation):
    try:
        patroller_json = resort.incident_template['DashboardItems']['field_52d47aac9bd13']
        patroller_dict = patroller_json['RepeatingQuestions']['patroller']['Values']

        try:
            updated = False
            for index, patroller in enumerate(patroller_dict):
                if patroller.keys()[0] == str(user.user_id):
                    if operation == 'add':
                        patroller_dict[index][str(user.user_id)] = user.name
                        updated = True
                    elif operation == 'remove':
                        patroller_dict.remove(patroller_dict[index])

            if not updated and operation == 'add':
                raise Exception('Not Found')
        except:
            patroller_dict.append({str(user.user_id): user.name})

        resort.incident_template['DashboardItems']['field_52d47aac9bd13'] = patroller_json
        resort.save()
    except:
        patroller_json = {
            "field_52d47aac9bd13": {
                "Label": "Patrollers",
                "Order": 84,
                "Required": "false",
                "RepeatingQuestions": {
                    "patroller": {
                        "Label": "Patroller",
                        "Placeholder": "",
                        "Type": "select",
                        "Required": "true",
                        "Order": 0,
                        "Values": [{str(user.user_id): user.name}]
                    },
                    "incident_role": {
                        "Label": "Incident Role",
                        "Placeholder": "",
                        "Type": "select",
                        "Required": "true",
                        "Order": 1,
                        "Values": [
                            {"170": "first_responder"},
                            {"171": "secondary"},
                            {"172": "assistant"},
                            {"173": "transport_assist"},
                            {"174": "base_assist"}
                        ]
                    }
                }
            }
        }

        resort.incident_template['DashboardItems'].update(patroller_json)
        resort.save()


def get_roleid_user(resort, user):
    user_resort = UserResortMap.objects.filter(resort=resort, user=user).first()

    if user_resort is not None:
        return user_resort.role.order
    else:
        return None


def register_user_mailchimp(list_id, email, resort_name, first_name, last_name, interest_list):
    http = urllib3.PoolManager()
    url = 'https://us3.api.mailchimp.com/3.0/lists/%s/members' % list_id
    data = {
        "email_address": email,
        "status": "pending",
        "email_type": "html",
        "merge_fields": {
            "FNAME": first_name,
            "LNAME": last_name,
            "RESORT": resort_name
        },
        "interests": {key: True for key in interest_list}
    }
    headers = {"Authorization": "Basic %s" % b64_encode("duncan:bf9fa3e09972580b286d55ed5edd6a02-us3"),
               "Content-Type": "application/json"}
    r = http.request('POST', url, headers=headers, body=json.dumps(data))


def validate_email(email):
    if pattern.match(email):
        return True
    else:
        return False
