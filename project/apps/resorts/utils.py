import validators

from apps.authentication.models import ResortOauthApp
from apps.custom_user.models import UserRoles
from apps.incidents.utils import get_template
from apps.resorts.models import Resort
from apps.resorts.models import UserResortMap
from apps.resorts.serializers import ResortSerializer
from apps.resorts.serializers import UserResortListSerializer
from apps.resorts.serializers import UserResortMapSerializer
from apps.routing.models import Domains
from helper_functions import delete_keys_from_dict
import urllib


def get_resort_by_name(resort_name):
    """
    Returns resort object based resort name
    """
    return Resort.objects.filter(resort_name=resort_name).first()


def get_resort_by_network_key(key):
    return Resort.objects.filter(network_key=key).first()


def get_resort_by_resort_id(key):
    return Resort.objects.filter(resort_id=key).first()


def get_user_resort_map(user, resort):
    return UserResortMap.objects.filter(user=user, resort=resort).first()


def get_resort_for_user(user):
    try:
        user_resort = UserResortMap.objects.filter(user=user).first()
        return user_resort.resort
    except:
        return None


def get_userrole_for_resort(resort, method, user):
    if user.user_connected == 1:
        user_resort_role = UserResortMap.objects.filter(resort=resort, user__user_connected=1, user__is_active=True)
    else:
        user_resort_role = UserResortMap.objects.filter(resort=resort, user=user, user__is_active=True)

    if len(user_resort_role) != 0:
        if method == 'get':
            user_resort_data = UserResortMapSerializer(user_resort_role, fields=('user', 'role'), many=True)
            return user_resort_data.data
        elif method == 'list':
            user_resort_data = UserResortListSerializer(user_resort_role, fields=('user', 'role'), many=True)
            return user_resort_data.data


def get_userrole_for_list(resort):
    user_resort_role = UserResortMap.objects.filter(resort=resort)

    if len(user_resort_role) != 0:
        user_resort_data = UserResortMapSerializer(user_resort_role, fields=('user', 'role'), many=True)
        return user_resort_data.data


def user_resort_map(user, resort, role_id):
    role = UserRoles(role_id=role_id)
    user_resort_exists = UserResortMap.objects.filter(user=user, resort=resort, role=role).first()

    if user_resort_exists is None:
        new_user_resort = UserResortMap(user=user, resort=resort, role=role)
        new_user_resort.save()

    return True


# Updates template of resort during creation and updation of resort
def template_update(resort, created):
    template = {}
    if created:
        template = get_template()
        if resort.print_on_device == 0:
            template = delete_keys_from_dict(template, ['print_button'])
    else:
        template = resort.incident_template
        if resort.print_on_device == 0:
            template = delete_keys_from_dict(template, ['print_button'])
        else:
            try:
                print_template = template['DashboardItems']['print_button']
            except:
                template['DashboardItems'].update({"print_button": {
                    "Label": "print",
                    "Placeholder": "",
                    "Type": "",
                    "Required": "false",
                    "Order": "9998",
                    "Values": ""
                }})
    return template


def get_setting_data_for_resort(resort):
    return_data = {}
    resort_data = ResortSerializer(resort, fields=('map_kml', 'default_unit_paper', 'map_lat', 'map_lng',
                                                   'network_key', 'licenses', 'report_form',
                                                   'unit_format', 'timezone', 'resort_logo', 'domain_id',
                                                   'datetime_format', 'dispatch_field_choice', 'initial_map_zoom_level'))
    return_data.update(resort_data.data)

    user_count = UserResortMap.objects.filter(resort=resort, user__user_connected=1, user__is_active=True).count()
    return_data.update({"user_count": user_count})

    try:
        app = ResortOauthApp.objects.get(resort=resort)
        return_data.update({'client_id': app.oauth_app.client_id, 'client_secret': app.oauth_app.client_secret})
    except:
        return_data.update({'client_id': '', 'client_secret': ''})


    return return_data


def transform_resort_settings_request(incoming_data):
    field_to_remove = []
    for key, value in incoming_data.iteritems():
        if key in ['resort_logo', 'map_kml', 'report_form']:
            if validators.url(value) or (not value):
                field_to_remove.append(key)

    for field in field_to_remove:
        del incoming_data[field]

    domain_id = incoming_data.get('domain_id')
    if domain_id is not None:
        domains = Domains.objects.filter(domain=domain_id)
        if len(domains) > 0:
            incoming_data['domain_id'] = domains[0].domain_id

    return incoming_data