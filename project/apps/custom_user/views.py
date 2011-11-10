import datetime
import json

import urllib3
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.query_utils import Q
from django.utils import timezone
from django.utils.translation import ugettext as _
from rest_framework import viewsets, mixins, generics, exceptions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import detail_route
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.authentication.custom_authentication_drf import OauthAuthentication
from apps.custom_user.models import UserConnected
from apps.custom_user.models import UserRoles
from apps.custom_user.serializers import UserResortSerializer
from apps.custom_user.serializers import UserRolesSerializer
from apps.custom_user.serializers import UserSerializer
from apps.custom_user.utils import get_devices_user
from apps.custom_user.utils import get_user_resort_combo
from apps.custom_user.utils import inject_patroller
from apps.custom_user.utils import register_user_mailchimp
from apps.custom_user.utils import user_has_permission
from apps.devices.models import Devices
from apps.devices.serializers import DeviceSerializer
from apps.resorts.models import UserResortMap, USER_DELETED, ARCHIVED, ACTIVE
from apps.resorts.serializers import ResortSerializer
from apps.resorts.utils import get_resort_by_network_key, get_resort_by_name, get_user_resort_map
from apps.resorts.utils import get_resort_by_resort_id
from apps.resorts.utils import get_resort_for_user
from apps.resorts.utils import user_resort_map
from apps.routing.models import Domains, RoutingUser
from apps.routing.models import RoutingCompany
from apps.routing.utils import update_user_discovery, remove_user_discovery
from helper_functions import construct_options


class Register(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (OauthAuthentication,)

    def post(self, request, format=None):
        user = None
        resort = None
        resort_created = False
        resort_map = None
        remote_request = True
        if settings.RUN_ENV != 'local':
            domain = Domains.objects.get(domain=request.get_host())
        else:
            domain = Domains.objects.get(pk=1)

        us_domain = Domains.objects.get(pk=1)
        au_domain = Domains.objects.get(pk=2)

        resort_network_key = request.data.get('resort_network_key', '')
        if resort_network_key:
            try:
                resort_map = RoutingCompany.objects.get(resort_token=resort_network_key)
            except:
                return Response({_('detail'): _('Resort with network key does not exist')}, status=400)

        country = request.data.get('country', '').lower()

        if resort_map is not None:
            if resort_map.domain == domain:
                remote_request = False

        # If user specified any of the below country then create resort and user in that particular region
        if country and country in ["australia", "new zealand"] and (domain == us_domain) and (
            settings.RUN_ENV != 'local') and remote_request:
            pool = urllib3.PoolManager()
            url = "https://" + au_domain.domain + "/api/v3/auth/register/"
            data = request.data
            header = {"Authorization": "Bearer sOMaRH33KEdmrLk2D6bdhaG13MjgY4", "Content-Type": "application/json"}

            # try creating resort in AU server. Returns error if anything went wild
            try:
                response = pool.urlopen('POST', url, headers=header, body=json.dumps(data))
                return Response(json.loads(response.data))
            except Exception as e:
                return Response(e.message, status=500)

        elif country and country not in ["australia", "new zealand"] and (domain == au_domain) and (
            settings.RUN_ENV != 'local') and remote_request:
            pool = urllib3.PoolManager()
            url = "https://" + us_domain.domain + "/api/v3/auth/register/"
            data = request.data
            header = {"Authorization": "Bearer sOMaRH33KEdmrLk2D6bdhaG13MjgY4", "Content-Type": "application/json"}

            # try creating resort in AU server. Returns error if anything went wild
            try:
                response = pool.urlopen('POST', url, headers=header, body=json.dumps(data))
                return Response(json.loads(response.data))
            except Exception as e:
                return Response(e.message, status=500)

        elif resort_map is not None and resort_map.domain != domain and (settings.RUN_ENV != 'local') and remote_request:
            pool = urllib3.PoolManager()
            url = "https://" + resort_map.domain.domain + "/api/v3/auth/register/"
            data = request.data
            header = {"Authorization": "Bearer sOMaRH33KEdmrLk2D6bdhaG13MjgY4", "Content-Type": "application/json"}

            # try creating resort in AU server. Returns error if anything went wild
            try:
                response = pool.urlopen('POST', url, headers=header, body=json.dumps(data))
                return Response(json.loads(response.data))
            except Exception as e:
                return Response(e.message, status=500)

        else:
            resort_name = request.data.get('resort_name')

            # First preference is given to the resort_network_key using which user can be connected to resort
            if resort_network_key is not None and resort_network_key:
                resort = get_resort_by_network_key(resort_network_key)
                if resort is None:
                    return Response({_('detail'): _('Resort with network key does not exist')}, status=400)
                else:
                    if resort.license_expiry_date is not None:
                        if resort.license_expiry_date < (timezone.now() + datetime.timedelta(hours=24)):
                            return Response({_('detail'): _('Resort expiry date past')}, status=400)

                    if resort.licenses is not None:
                        if UserResortMap.objects.filter(resort=resort, user__is_active=True,
                                                        user__user_connected=1).count() >= resort.licenses:
                            return Response({_('detail'): _('no more licenses')}, status=400)
                user_connected = 1

            # Second preference for connecting user to resort is given to the resort_name
            # If resort with provided resort_name doesn't exists then new one is created
            elif resort_name is not None and resort_name:
                resort = get_resort_by_name(resort_name)
                if resort is None:
                    resort_data = ResortSerializer(data=request.data)

                    if resort_data.is_valid():
                        resort = resort_data.save(domain_id=domain)
                        resort_created = True
                    else:
                        return Response(resort_data.errors, status=400)
                user_connected = 0
            else:
                return Response({_('detail'): _('resort name and/or resort network key not provided')}, status=400)

            # Try to get existing user and if it doesn't find then create new user
            try:
                user = get_user_model().objects.get(email__iexact=request.data.get('email'))
                return Response({_('detail'): _('the email address is already in use')}, status=403)
                # user_data = UserSerializer(user, data=request.data, partial=True)
            except:
                user_data = UserSerializer(data=request.data, fields=('email', 'phone', 'name', 'password'))

            if user_data.is_valid():
                user = user_data.save(user_connected=user_connected, is_active=True)
                if settings.RUN_ENV == 'master':
                    register_user_mailchimp('c08200b7c1', user.email, resort.resort_name, user.name, "", ['11182343c6'])
                else:
                    register_user_mailchimp('c08200b7c1', user.email, resort.resort_name, user.name, "", ['0005c6dcdf'])
            else:
                return Response(user_data.errors, status=400)

            # Create user and resort mapping and uses default role of patroller for newly created user
            user_resort_map, created = UserResortMap.objects.get_or_create(user=user, resort=resort,
                                                                           defaults={
                                                                               'role': UserRoles.objects.get(pk=1)})

            if user_connected == 1:
                inject_patroller(resort, user, 'add')

            # Creates new device
            data = request.data
            data['device_user'] = user.user_pk
            device_data = DeviceSerializer(data=data)

            if device_data.is_valid():
                device = device_data.save()
            else:
                return Response(device_data.errors, status=400)

            # Gets token of newly created user
            token = Token.objects.get(user=user)

            # Updates user discovery table across the cluster
            try:
                update_user_discovery(user, resort.domain_id, request)
            except Exception as e:
                return Response(e.message, status=500)

            return Response({
                "resort_id": resort.resort_id,
                "resort_name": resort.resort_name,
                "user_id": user.user_id,
                "device_id": device.device_id,
                "token": token.key,
                "user_connected": construct_options(UserConnected, user_connected)
            })


class RolesUser(APIView):
    renderer_classes = (JSONRenderer,)

    def get(self, request, format=None):
        response_data = {}
        roles = UserRoles.objects.all()
        roles = UserRolesSerializer(roles, many=True)
        response_data["count"] = len(roles.data)
        response_data["results"] = roles.data
        return Response(response_data, status=200)


class UserViewSet(viewsets.ViewSet, mixins.ListModelMixin, generics.GenericAPIView):
    def create(self, request):
        resort_id = request.data.get('resort_id')
        resort = get_resort_by_resort_id(resort_id)
        role_id = request.data.get('role_id')

        # If role_id not provided (or) empty then use default role_id as 1 (patroller)
        if (role_id is None) and (not role_id):
            role_id = 1
        elif not (0 < role_id < 4):
            return Response({_('detail'): _("invalid role_id provided")}, status=400)

        if resort is not None:
            if resort.licenses is not None:
                if UserResortMap.objects.filter(resort=resort, user__is_active=True,
                                                user__user_connected=1).count() >= resort.licenses:
                    return Response({_('detail'): _('no more licenses')}, status=400)

            if user_has_permission(request.user, resort, 3) or request.user.is_admin:
                try:
                    user = get_user_model().objects.get(email__iexact=request.data.get('email').lower())
                    return Response({_('detail'): _('the email address is already in use')}, status=403)
                    # user_data = UserSerializer(user, data=request.data, partial=True)
                except:
                    user_data = UserSerializer(data=request.data, fields=('email', 'phone', 'name', 'password'))

                if user_data.is_valid():
                    user = user_data.save(user_connected=1, is_active=True)
                    if settings.RUN_ENV == 'master':
                        register_user_mailchimp('c08200b7c1', user.email, resort.resort_name, user.name, "",
                                                ['11182343c6'])
                    else:
                        register_user_mailchimp('c08200b7c1', user.email, resort.resort_name, user.name, "",
                                                ['0005c6dcdf'])
                else:
                    return Response(user_data.errors, status=400)

                inject_patroller(resort, user, 'add')
            else:
                return Response({_('detail'): _("You dont have have permission to add user")}, status=403)
        else:
            return Response({_("detail"): _("Resort with provided resort_id does not exists")}, status=400)

        update_user_discovery(user, resort.domain_id, request)

        user_resort_map(user, resort, role_id)

        response_data = get_user_resort_combo(user.user_pk, ('resort_id', 'resort_name', 'map_kml', 'map_type',
                                                             'report_form', 'unit_format', 'timezone', 'map_lat',
                                                             'map_lng', 'resort_logo', 'datetime_format',
                                                             'resort_controlled_substances',
                                                             'resort_asset_management'))

        return Response(response_data, status=200)

    def update(self, request, pk=None):

        try:
            user = get_user_model().objects.get(user_id=pk)
        except:
            return Response({_("detail"): _("User does not exists")}, status=400)

        resort = get_resort_for_user(user)

        if user_has_permission(request.user, resort, 3) or request.user == user or request.user.is_admin:
            if not user.is_active:
                return Response({_("detail"): _("User inactive or deleted.")}, status=403)

            user_data = UserSerializer(user, data=request.data, partial=True)

            if user_data.is_valid():
                routing_user = RoutingUser.objects.filter(email=user_data.validated_data['email']).first()
                if routing_user is not None:
                    if user_data.validated_data['email'] != user.email:
                        return Response({_("detail"): _('the email address is already in use')}, status=403)
                else:
                    # Remove previous user information from discovery table across all region
                    remove_user_discovery(user, resort.domain_id, request)

                user = user_data.save()
                if user.user_connected == 1:
                    inject_patroller(resort, user, 'add')
                else:
                    inject_patroller(resort, user, 'remove')

                role = request.data.get('role_id')
                if role is not None and role:
                    user_resort = UserResortMap.objects.filter(user=user, resort=resort).first()
                    if user_resort is not None:
                        role = UserRoles.objects.filter(role_id=role).first()
                        if role is not None:
                            user_resort.role = role
                            user_resort.save()
                        else:
                            return Response({_("detail"): _("specified role does not exists")}, status=400)

                if routing_user is None:
                    # Update user email and Name across all the region
                    update_user_discovery(user, resort.domain_id, request)

                    # Update mailchimp with new user
                    if settings.RUN_ENV == 'master':
                        register_user_mailchimp('c08200b7c1', user.email, resort.resort_name, user.name, "",
                                                    ['11182343c6'])
                    else:
                        register_user_mailchimp('c08200b7c1', user.email, resort.resort_name, user.name, "",
                                                ['0005c6dcdf'])
            else:
                return Response(user_data.errors, status=400)
        else:
            return Response({_("detail"): _("You don't have permission to update user")}, status=403)

        response_data = get_user_resort_combo(user.user_pk, ('resort_id', 'resort_name', 'map_kml', 'map_type',
                                                             'report_form', 'unit_format', 'timezone', 'map_lat',
                                                             'map_lng', 'resort_logo', 'datetime_format',
                                                             'resort_controlled_substances', 'resort_asset_management'))
        return Response(response_data, status=200)

    def retrieve(self, request, pk=None):
        from apps.custom_user.utils import get_user_resort_status
        try:
            user = get_user_model().objects.get(user_id=pk)
        except:
            return Response({_("detail"): _("User does not exists")}, status=400)

        resort = get_resort_for_user(user)

        if (user_has_permission(request.user, resort, 3) or user_has_permission(request.user, resort,
                                                                                2)) or request.user == user or request.user.is_admin:
            if not user.is_active:
                return Response({_("detail"): _("User inactive or deleted.")}, status=403)
            response_data = get_user_resort_combo(user.user_pk, ('resort_id', 'resort_name', 'map_kml', 'map_type',
                                                                 'report_form', 'unit_format', 'timezone', 'map_lat',
                                                                 'map_lng', 'resort_logo', 'datetime_format',
                                                                 'resort_controlled_substances',
                                                                 'resort_asset_management'))
            response_data.update({"user_status": get_user_resort_status(user, resort)})
            return Response(response_data, status=200)
        else:
            return Response({_("detail"): _("You dont have permission to retrieve user")}, status=403)

    def destroy(self, request, pk=None):

        try:
            user = get_user_model().objects.get(user_id=pk)
        except:
            return Response({_("detail"): _("User does not exists")}, status=400)

        resort = get_resort_for_user(user)
        response_data = {}

        if user_has_permission(request.user, resort, 3) or request.user.is_admin:
            user_resort_map_combo = get_user_resort_map(user, resort)
            user_resort_map_combo.user_status = USER_DELETED
            user_resort_map_combo.save()

            if not user.is_active:
                return Response({_("detail"): _("User inactive or deleted.")}, status=403)

            user.is_active = False
            user.save()
            response_data['user_id'] = user.user_id
            response_data['status'] = 'deleted'

            # Deletes all the device associated with user
            Devices.objects.filter(device_user=user).delete()

            inject_patroller(resort, user, 'remove')

            return Response(response_data, status=200)
        else:
            return Response({_("detail"): _("You dont have permission to delete user")}, status=403)

    @detail_route()
    def status(self, request, pk=None):
        status_type = request.query_params.get('type', 'activate')
        resort_id = request.query_params.get('resort_id', '')

        try:
            status_user = get_user_model().objects.get(user_id=pk)
        except:
            return Response({_("detail"): _("User does not exists")}, status=400)

        request_user = request.user
        status_user_resort = get_resort_for_user(status_user)
        request_user_resort = get_resort_for_user(request_user)

        if (status_user_resort != request_user_resort) or str(status_user_resort.resort_id) != resort_id:
            raise exceptions.PermissionDenied

        if user_has_permission(request_user, request_user_resort, 3) or request.user.is_admin:
            status_user_resort_map = get_user_resort_map(status_user, status_user_resort)

            status_user_resort_map.user_status = ARCHIVED if status_type == 'archived' else ACTIVE
            status_user_resort_map.save()

            return Response({_("detail"): _("user status updated")}, status=200)
        else:
            raise exceptions.PermissionDenied

    def list(self, request, *args, **kwargs):
        user = self.request.user
        search = request.query_params.get('search', '')
        order_by = request.query_params.get('order_by', 'user__name')
        order_by_direction = request.query_params.get('order_by_direction', 'desc')
        user_resort = UserResortMap.objects.filter(user=user).first()

        if order_by_direction == 'desc':
            order = '-' + order_by
        elif order_by_direction == 'asc':
            order = order_by

        if user_has_permission(request.user, user_resort.resort, 3) or request.user.is_admin:
            user_id = []
            query = None
            if user.is_admin:
                query = UserResortMap.objects.filter(Q(user__email__icontains=search) | Q(user__name__icontains=search),
                                                     user__is_active=True).order_by(order)
            else:
                query = UserResortMap.objects.filter(Q(user__email__icontains=search) | Q(user__name__icontains=search),
                                                     resort=user_resort.resort, user__is_active=True,
                                                     user__user_connected=user.user_connected).order_by(order)

            queryset = self.filter_queryset(query)

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = UserResortSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({_("detail"): _("You dont have permission to list user")}, status=403)

    @detail_route()
    def devices(self, request, pk=None):
        user = request.user
        resort = get_resort_for_user(user)
        response_data = {}

        if user_has_permission(request.user, resort, 3) or request.user == user or request.user.is_admin:
            user = get_user_model().objects.filter(user_id=pk).first()

            if user is not None:
                if not user.is_active:
                    return Response({_("detail"): _("User inactive or deleted.")}, status=403)

                device_data = get_devices_user(user)
                response_data['device_count'] = len(device_data)
                response_data['user_id'] = user.user_id
                response_data['devices'] = device_data

                return Response(response_data, status=200)
            else:
                return Response({_('detail'): _('user does not exists')}, status=400)
        else:
            return Response({_("detail"): _("You dont have permission to retrieve user device")}, status=403)
