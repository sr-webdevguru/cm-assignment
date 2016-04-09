import json

import urllib3
from django.conf import settings

from apps.routing.models import Domains
from apps.routing.models import RoutingUser, RoutingCompany
from apps.routing.serializers import RoutingUserSerializer, RoutingCompanySerializer


def update_user_discovery(user, domain, request):
    user_route = RoutingUser.objects.filter(email=user.email).first()

    if user_route is None:
        new_user_route = RoutingUser(email=user.email, domain=domain)
        new_user_route.save()
    else:
        user_route.domain = domain
        user_route.save()
        new_user_route = user_route

    if settings.RUN_ENV != 'local':
        user_route_data = RoutingUserSerializer(new_user_route, fields=('domain', 'email'))
        domains = Domains.objects.all().exclude(domain=request.get_host()).filter(is_active=True)

        for domain in domains:
            pool = urllib3.PoolManager()
            url = "https://" + domain.domain + "/api/v3/sync/"
            data = {"type": "user", "operation": "add", "data": user_route_data.data}
            header = {"Content-Type": "application/json"}
            response = pool.urlopen('POST', url, headers=header, body=json.dumps(data))
    return True


def remove_user_discovery(user, domain, request):
    user_route = RoutingUser.objects.filter(email=user.email).first()

    if user_route is not None:
        if settings.RUN_ENV != 'local':
            user_route_data = RoutingUserSerializer(user_route, fields=('domain', 'email'))
            domains = Domains.objects.all().exclude(domain=request.get_host()).filter(is_active=True)

            for domain in domains:
                pool = urllib3.PoolManager()
                url = "https://" + domain.domain + "/api/v3/sync/"
                data = {"type": "user", "operation": "remove", "data": user_route_data.data}
                header = {"Content-Type": "application/json"}
                response = pool.urlopen('POST', url, headers=header, body=json.dumps(data))

            user_route.delete()
    return True


def update_resort_discovery(resort, domain):
    resort_route = RoutingCompany.objects.filter(resort_token=resort.network_key).first()

    if resort_route is None:
        new_resort_route = RoutingCompany(resort_token=resort.network_key,
                                          resort_name=resort.resort_name,
                                          domain=domain)
        new_resort_route.save()
    else:
        resort_route.domain = domain
        resort_route.resort_name = resort.resort_name
        resort_route.save()
        new_resort_route = resort_route

    if settings.RUN_ENV != 'local':
        resort_route_data = RoutingCompanySerializer(new_resort_route, fields=('resort_name', 'resort_token', 'domain'))
        domains = Domains.objects.all().exclude(domain=new_resort_route.domain.domain).filter(is_active=True)

        for domain in domains:
            pool = urllib3.PoolManager()
            url = "https://" + domain.domain + "/api/v3/sync/"
            data = {"type": "resort", "data": resort_route_data.data}
            header = {"Content-Type": "application/json"}
            response = pool.urlopen('POST', url, headers=header, body=json.dumps(data))

    return True
