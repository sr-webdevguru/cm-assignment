import base64
import csv
import json
import os

from django.conf import settings

from apps.data_sync.models import Language
from apps.routing.models import Domains
from apps.routing.models import RoutingCompany
from apps.routing.models import RoutingUser
from apps.routing.serializers import RoutingCompanySerializer
from apps.routing.serializers import RoutingUserSerializer


def handle_uploaded_file(f):
    with open('a.csv', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def update_language(data):
    new_language_update = Language(language_data=data['csv'])
    new_language_update.save()

    with open('a.csv', 'w+') as destination:
        destination.write(base64.b64decode(data['csv']))

    json_file_path = os.path.join(settings.STATIC_ROOT, 'language')

    if not os.path.exists(json_file_path):
        os.makedirs(json_file_path)

    with open(os.path.join(json_file_path, 'en.json'), 'w+') as jsonfile:
        with open('a.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = {}
            for index, row in enumerate(reader):
                if index > 1:
                    data.update({row[2]: row[5]})
            jsonfile.write(json.dumps(data))

    return new_language_update.id


def update_user_map(data, operation):
    domain = Domains.objects.get(pk=data['domain'])
    if operation == 'add':
        try:
            routing_user = RoutingUser.objects.get(email=data['email'])
            routing_user_data = RoutingUserSerializer(routing_user, data=data, partial=True)
            if routing_user_data.is_valid():
                user_discovery = routing_user_data.save(domain=domain)
            else:
                return routing_user_data.errors
        except:
            routing_user_data = RoutingUserSerializer(data=data)
            if routing_user_data.is_valid():
                user_discovery = routing_user_data.save(domain=domain)
            else:
                return routing_user_data.errors
        return user_discovery
    elif operation == 'remove':
        routing_user = RoutingUser.objects.filter(email=data['email']).delete()
        return routing_user


def update_resort_map(data):
    domain = Domains.objects.get(pk=data['domain'])
    try:
        routing_company = RoutingCompany.objects.get(resort_token=data['resort_token'])
        routing_company_data = RoutingCompanySerializer(routing_company, data=data, partial=True)
        if routing_company_data.is_valid():
            routing_company = routing_company_data.save(domain=domain)
        else:
            return routing_company_data.errors
    except:
        routing_company_data = RoutingCompanySerializer(data=data)
        if routing_company_data.is_valid():
            routing_company = routing_company_data.save(domain=domain)
        else:
            return routing_company_data.errors
    return routing_company
