import datetime
import json

import urllib3
from django.conf import settings
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.http.request import QueryDict
from django.http.response import JsonResponse
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from rest_framework import exceptions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from validators.uuid import uuid

from apps.authentication.custom_authentication_drf import OauthAuthentication
from apps.authentication.models import ResortOauthApp
from apps.custom_user.utils import get_devices_user
from apps.custom_user.utils import get_roleid_user
from apps.custom_user.utils import get_token
from apps.custom_user.utils import get_user_resort_combo
from apps.custom_user.utils import user_has_permission
from apps.custom_user.utils import validate_email
from apps.devices.models import Devices, Heartbeat
from apps.devices.serializers import DeviceSerializer
from apps.resorts.models import ACTIVE
from apps.resorts.utils import get_resort_for_user
from apps.routing.models import RoutingUser
from oauth2_provider.models import Application

ENV_MAPPING = {
    'master': 'X',
    'dev': 'Y',
    'staging': 'Z'
}

COUNTRY_MAPPING = {
    'us': 1,
    'au': 2,
    'ca': 3
}

FRONTEND_MAPPING = {
    'X': 'app.medic52.com',
    'Y': 'app-dev.medic52.com',
    'Z': 'app-staging.medic52.com'
}


@api_view()
@permission_classes((AllowAny,))
@authentication_classes((OauthAuthentication,))
def entry_point(request):
    return Response({"v3"}, status=200)


@api_view()
@permission_classes((AllowAny,))
@authentication_classes((OauthAuthentication,))
def version_entry_point(request):
    url = settings.SCHEME + request.get_host() + "/api/v3/auth/discover/"
    return Response({"auth.discover": url}, status=200)


class Login(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (OauthAuthentication,)

    def post(self, request, format=None):
        from apps.resorts.utils import get_user_resort_map
        email = request.data.get('email')
        password = request.data.get('password')
        device_id = request.data.get('device_id')
        response_data = {}

        # if both email and password has been provided and its not empty
        if email is not None and password is not None and email and password:
            # Validates email format and returns error if invalid format
            try:
                email_name, domain_part = request.data.get('email').strip().rsplit('@', 1)
                email = '@'.join([email_name.lower(), domain_part.lower()])
                if not validate_email(email):
                    return Response({_("detail"): _("invalid email provided")}, status=400)
            except:
                return Response({_("detail"): _("invalid email provided")}, status=400)

            # Authenticates user using email as username and password
            user = authenticate(username=email, password=password)

            # If it authenticates user then an user object would be returned
            if user is not None:

                user_resort = get_resort_for_user(user)

                user_resort_map = get_user_resort_map(user, user_resort)

                if user_resort_map.user_status != ACTIVE:
                    raise Response({_('detail'): _('you_cannot_login_account_is_disabled')}, status=403)

                # device_id is not provided and device_type and device_os is provided then new device is created
                if device_id is None and (request.data.get('device_type') is not None or
                                                  request.data.get('device_os') is not None or
                                                  request.data.get('device_push_token') is not None):
                    new_device = DeviceSerializer(data=request.data,
                                                  fields=('device_type', 'device_os', 'device_push_token'))
                    # validates device data and returns error if any
                    if new_device.is_valid():
                        new_device = new_device.save(device_user=user)
                        device_id = new_device.device_id
                    else:
                        return Response(new_device.errors, status=400)

                if user_resort is not None:
                    if user_resort.license_expiry_date is not None:
                        if user_resort.license_expiry_date < (timezone.now() + datetime.timedelta(hours=24)):
                            return Response({_('detail'): _('Resort expiry date past')}, status=400)

                # Logs user into the system
                login(request, user)

                # Get resort associated with user and pass if we don't find any
                try:
                    resort_data = get_user_resort_combo(user.user_pk,
                                                        ('resort_id', 'resort_name', 'map_kml', 'map_type',
                                                         'report_form', 'unit_format', 'timezone', 'map_lat', 'map_lng',
                                                         'resort_logo', 'datetime_format',
                                                         'resort_controlled_substances',
                                                         'resort_asset_management'))
                    response_data.update(resort_data)
                except:
                    pass

                response_data.update({'token': get_token(user)})

                if device_id is not None:
                    response_data.update({'device_id': device_id})
                return Response({'user': response_data})
            else:
                return Response({_('detail'): _(
                    'Your username or password are not correct please try again or click to retrieve your password')},
                    status=403)
        else:
            return Response({_('detail'): _('email/password is not provided')}, status=400)


class Logout(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (OauthAuthentication,)

    def post(self, request, format=None):
        logout(request)
        return Response({'detail': _("User is logged out")}, status=200)


class CustomPasswordResetForm(PasswordResetForm):
    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        # sub_domain = request.get_host().split('.')[0]

        email = self.cleaned_data["email"].lower()

        user_map = RoutingUser.objects.get(email=email)

        host = request.get_host()

        if host != user_map.domain.domain:
            pool = urllib3.PoolManager()
            url = "https://" + user_map.domain.domain + "/api/v3/auth/password_reset/"
            data = {'email': email}
            header = {"Authorization": "Bearer sOMaRH33KEdmrLk2D6bdhaG13MjgY4", "Content-Type": "application/json"}

            # try creating resort in AU server. Returns error if anything went wild
            try:
                response = pool.urlopen('POST', url, headers=header, body=json.dumps(data))
            except Exception as e:
                pass
        else:

            sub_domain = user_map.domain.domain.split('.')[0]

            try:
                env = ENV_MAPPING[sub_domain.split('-')[1]]
            except:
                env = ENV_MAPPING['master']

            if env == 'X':
                region = COUNTRY_MAPPING[sub_domain.split('-')[1]]
            else:
                region = COUNTRY_MAPPING[sub_domain.split('-')[2]]

            domain = FRONTEND_MAPPING[env]

            for user in self.get_users(email):
                context = {
                    'email': user.email,
                    'domain': domain,
                    'site_name': 'Medic52',
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'user': user,
                    'token': token_generator.make_token(user),
                    'protocol': 'https',
                    'server_id': env + str(region)
                }

                self.send_mail(subject_template_name, email_template_name,
                               context, from_email, user.email,
                               html_email_template_name=html_email_template_name)


@never_cache
def password_reset_final(request, uidb64=None, token=None,
                         template_name='registration/password_reset_confirm.html',
                         token_generator=default_token_generator,
                         set_password_form=SetPasswordForm,
                         post_reset_redirect=None,
                         current_app=None, extra_context=None):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    UserModel = get_user_model()
    assert uidb64 is not None and token is not None  # checked by URLconf
    try:
        # urlsafe_base64_decode() decodes to bytestring on Python 3
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        title = _('Enter new password')
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({_('detail'): _('password reset successful')}, status=200)
        else:
            form = set_password_form(user)
    else:
        return JsonResponse({_('detail'): _('password link is invalid (or) expired')}, status=400)


# This snipped is taken from django to modify its behaviour
@api_view(['POST'])
@permission_classes((AllowAny,))
@authentication_classes((OauthAuthentication,))
def password_reset(request, is_admin_site=False,
                   template_name='registration/password_reset_form.html',
                   email_template_name='password_reset/password_reset_email.html',
                   subject_template_name='password_reset/password_reset_subject.txt',
                   password_reset_form=CustomPasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email='duncan@medic52.com',
                   current_app=None,
                   extra_context=None,
                   html_email_template_name=None):
    if request.method == "POST":

        # Validates email and returns error if invalid
        try:
            email_name, domain_part = request.data.get('email').strip().rsplit('@', 1)
            email = '@'.join([email_name, domain_part.lower()])
            if not validate_email(email):
                return Response({_("detail"): _("invalid email provided")}, status=400)
        except:
            return Response({_("detail"): _("invalid email provided")}, status=400)

        a = QueryDict('email=' + email)
        form = password_reset_form(a)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
                'html_email_template_name': html_email_template_name,
            }
            form.save(**opts)
            return Response({_("detail"): _("Email to reset password has been sent")})
    else:
        form = password_reset_form()
    context = {
        'form': form,
        'title': 'Password reset',
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


@api_view(['GET'])
@permission_classes((AllowAny,))
@authentication_classes((OauthAuthentication,))
def password_reset_token_check(request, uidb64=None, token_generator=default_token_generator, token=None):
    UserModel = get_user_model()
    # Get user from provided uid
    try:
        # urlsafe_base64_decode() decodes to bytestring on Python 3
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if token is None and user is None:
        return Response({_('detail'): _('token or uid not provided')}, status=400)

    if token_generator.check_token(user, token):
        return Response({_('detail'): _('valid password reset token')}, status=200)
    else:
        return Response({_('detail'): _('invalid password reset token')}, status=400)


class OauthApp(APIView):
    def post(self, request, *args, **kwargs):

        user = request.user
        resort = get_resort_for_user(user)
        operation = request.GET.get('operation', 'generate')

        # Only manager has the permission to access the resource
        if resort is not None:
            role = get_roleid_user(resort=resort, user=user)
            if role != 3:
                return Response({_('detail'): _('you do not have permission to resource')}, status=400)
        else:
            return Response({_('detail'): _('no resort associated with user')}, status=400)

        if operation == 'generate':
            # If oauth app already exists then return existing credential
            try:
                app = ResortOauthApp.objects.get(resort=resort, is_active=True)
                app = app.oauth_app
            except:
                app = Application(user=user, authorization_grant_type='client-credentials', client_type='confidential',
                                  name=resort.resort_name)
                app.save()

                resort_oauth = ResortOauthApp(resort=resort, oauth_app=app)
                resort_oauth.save()
        elif operation == 'regenerate':
            try:
                app = ResortOauthApp.objects.get(resort=resort, is_active=True)
                oauth_app = app.oauth_app
                oauth_app.delete()
            except:
                pass

            app = Application(user=user, authorization_grant_type='client-credentials', client_type='confidential',
                              name=resort.resort_name)
            app.save()

            resort_oauth = ResortOauthApp(resort=resort, oauth_app=app)
            resort_oauth.save()

        return Response({'client_id': app.client_id, 'client_secret': app.client_secret}, status=200)


class Impersonate(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        resort = get_resort_for_user(user)

        # Check if the user requesting the impersonate is manager (or) not.
        if not user_has_permission(user, resort, 3):
            return Response({_('detail'): _('you do not have permission to impersonate this user')}, status=400)

        # check for validity of the UUID of the user
        if not uuid(kwargs['user_id']):
            return Response({_('detail'): _('not a valid UUID')}, status=400)

        device_id = request.query_params.get('device_id')
        if device_id is None:
            return Response({_('detail'): _('device_id not provided')}, status=400)

        try:
            impersonate_user = get_user_model().objects.get(user_id=kwargs['user_id'])
            impersonate_user_resort = get_resort_for_user(impersonate_user)

            if impersonate_user_resort != resort:
                return Response({_('detail'): _('user is not allowed to impersonate')}, status=400)
        except:
            return Response({_('detail'): _('user not found')}, status=400)

        try:
            device = Devices.objects.get(device_id=device_id)
        except:
            return Response({_('detail'): _('device with provided device_id does not exists')}, status=400)

        try:
            Heartbeat.objects.get(user=impersonate_user, device=device)
        except:
            heartbeat = Heartbeat(user=impersonate_user, device=device)
            heartbeat.save()

        response_data = {}
        resort_data = get_user_resort_combo(impersonate_user.user_pk,
                                            ('resort_id', 'resort_name', 'map_kml', 'map_type',
                                             'report_form', 'unit_format', 'timezone', 'map_lat', 'map_lng',
                                             'datetime_format', 'season_start_date', 'dispatch_field_choice'),
                                            ('user_id', 'name', 'email', 'phone'))
        response_data.update(resort_data)
        response_data.update({'devices': get_devices_user(impersonate_user)})
        response_data.update({'token': get_token(impersonate_user)})

        return Response(response_data, status=200)
