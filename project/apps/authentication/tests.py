import json

from django.test import TestCase
from django.test.client import Client
from rest_framework.test import APITestCase, APIClient

from apps.authentication.factory.oauth_factory import ApplicationFactory
from apps.authentication.factory.oauth_factory import TokenFactory
from apps.custom_user.factory.user_factory import UserFactory
from apps.custom_user.factory.user_factory import UserRolesFactory
from apps.resorts.factory.resort_factory import IncidentTemplateFactory, UserResortMapFactory, ResortFactory
from apps.routing.factory.routing_factory import DomainFactory, RoutingUserFactory

class Oauth2TestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.application = ApplicationFactory()
        self.domain = DomainFactory(domain_id=1)
        self.domain = DomainFactory(domain_id=2, domain='api-dev-au.medic52.com', is_active=True)
        self.domain = DomainFactory(domain_id=3, domain='testserver', is_active=True)
        self.incidentTemplate = IncidentTemplateFactory(template_id=1)
        self.resort = ResortFactory(resort_name='Vanilla Ski', license_expiry_date='2018-04-01T00:00:00', licenses=5)
        self.userRoles = UserRolesFactory()
        self.userRoles = UserRolesFactory(role_id=2, key='dispatcher', order=2)
        self.userRoles = UserRolesFactory(role_id=3, key='manager', order=3)
        self.user_resort_map = UserResortMapFactory(role_id=3, user=self.user, resort=self.resort)
        self.c = Client()

    def testAccessToken(self):
        response = self.client.post('/oauth/access_token/',
                                    {'grant_type': 'client_credentials', 'client_id': self.application.client_id,
                                     'client_secret': self.application.client_secret})
        response_json = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['token_type'], "Bearer")
        self.assertEqual(response_json['expires_in'], 1800)
        self.assertEqual(response_json['scope'], "read write")

    def testInvalidClientInfo(self):
        response = self.client.post('/oauth/access_token/',
                                    {'grant_type': 'client_credentials', 'client_id': '', 'client_secret': ''})
        response_json = json.loads(response.content)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_json['error'], "invalid_client")

    def testInvalidClientCredential(self):
        response = self.client.post('/oauth/access_token/',
                                    {'grant_type': 'client_credential', 'client_id': self.application.client_id,
                                     'client_secret': self.application.client_secret})
        response_json = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['error'], "unsupported_grant_type")


class LoginTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.application = ApplicationFactory()
        self.routing_user = RoutingUserFactory(email='jerol@lycos.com')
        self.domain = DomainFactory(domain_id=1)
        self.incidentTemplate = IncidentTemplateFactory(template_id=1)
        self.resort = ResortFactory(resort_name='Vanilla Ski', license_expiry_date='2018-04-01T00:00:00', licenses=5)
        self.userRoles = UserRolesFactory()
        self.userRoles = UserRolesFactory(role_id=2, key='dispatcher', order=2)
        self.userRoles = UserRolesFactory(role_id=3, key='manager', order=3)
        self.user_resort_map = UserResortMapFactory(role_id=3, user=self.user, resort=self.resort)
        self.c = APIClient()
        self.token = TokenFactory(user=self.user)

    def testMobileLogin(self):
        response = self.client.post('/oauth/access_token/',
                                    {'grant_type': 'client_credentials', 'client_id': self.application.client_id,
                                     'client_secret': self.application.client_secret})
        # print response.content
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')
        # print response.data
        self.assertEqual(response.data['user']['token'], self.token.key)

    def testMobileLoginNewDevice(self):
        # test user login
        response = self.client.post('/oauth/access_token/',
                                    {'grant_type': 'client_credentials', 'client_id': self.application.client_id,
                                     'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234',
                                                       # 'device_os': 'iOS 7.0.2', 'device_type': 'iPhone 6',
                                                       'device_push_token': 'dsadsadjeoqiry38ioqwdksdn'}, format='json')
        self.user_id = str(self.user.user_id)
        # self.assertEqual(response.data['user']['user_id'], self.user_id)
        self.assertEqual(response.status_code, 400)

        # email or password not provided in login
        response = self.c.post('/api/v3/auth/login/', {'device_os': 'iOS 7.0.2', 'device_type': 'iPhone 6',
                                                       'device_push_token': 'dsadsadjeoqiry38ioqwdksdn'}, format='json')
        self.assertEqual(response.data['detail'], 'email_password_is_not_provided')

        # invalid email provided in login
        response = self.c.post('/api/v3/auth/login/', {'email': "jerol.com", 'password': '1234'}, format='json')
        response_json = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['detail'], "invalid_email_provided")

        # incorrect email or password in login
        response = self.c.post('/api/v3/auth/login/', {'email': "jerol@lycos.com", 'password': '1234'}, format='json')
        response_json = json.loads(response.content)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_json['detail'],
                         "your_username_or_password_are_not_correct_please_try_again_or_click_to_retrieve_your_password")

    def testMobileResetPassword(self):
        response = self.client.post('/oauth/access_token/',
                                    {'grant_type': 'client_credentials', 'client_id': self.application.client_id,
                                     'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234',
                                                       'device_os': 'iOS 7.0.2', 'device_type': 'iPhone 6',
                                                       'device_push_token': 'dsadsadjeoqiry38ioqwdksdn'}, format='json')
        # invalid email provided in reset password
        response = self.c.post('/api/v3/auth/password_reset/', {'email': "jerol.lycos.com"}, format='json')
        response_json = json.loads(response.content)
        self.assertEqual(response_json['detail'], "invalid_email_provided")

        # successful password reset
        response = self.c.post('/api/v3/auth/password_reset/', {'email': "jerol@lycos.com"}, format='json')
        response_json = json.loads(response.content)
        self.assertEqual(response_json['detail'], "email_to_reset_password_has_been_sent")

    def testMobileLogout(self):
        response = self.client.post('/oauth/access_token/',
                                    {'grant_type': 'client_credentials', 'client_id': self.application.client_id,
                                     'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')
        self.user_id = str(self.user.user_id)
        response = self.c.post('/api/v3/auth/logout/' + self.user_id, {})
        response_json = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['detail'], "user_is_logged_out")


from apps.authentication.exceptions import NotFoundException


class ExceptionsTestCase(APITestCase):
    def testException(self):
        self.exception = NotFoundException("user")
        self.assertEqual(self.exception.detail, "user not found")
        self.assertEqual(self.exception.status_code, 400)


from django.test.client import RequestFactory
from rest_framework.request import Request
from health_check_cache.plugin_health_check import CacheBackend
from health_check_db.plugin_health_check import DjangoDatabaseBackend
from health_check_storage.plugin_health_check import DefaultFileStorageHealthCheck
from apps.authentication.health_check import healthcheck


class HealthCheckTestCase(APITestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def testHealthCheck(self):
        request = self.factory.get('/?type=db')
        request = Request(request)
        # print "debug>>", request.query_params['type'], "<<debug"
        plugin = DjangoDatabaseBackend()
        # print plugin.status, "debug"
        response = healthcheck(request)
        response.render()
        response_json = json.loads(response.content)
        self.assertEqual(response_json['status'], plugin.pretty_status())

        request = self.factory.get('/?type=cache')
        request = Request(request)
        # print "debug>>", request.query_params['type'], "<<debug"
        plugin = CacheBackend()
        # print plugin.status, "debug"
        response = healthcheck(request)
        response.render()
        response_json = json.loads(response.content)
        self.assertEqual(response_json['status'], plugin.pretty_status())

        request = self.factory.get('/?type=storage')
        request = Request(request)
        # print "debug>>", request.query_params['type'], "<<debug"
        plugin = DefaultFileStorageHealthCheck()
        # print plugin.status, "debug"
        response = healthcheck(request)
        response.render()
        response_json = json.loads(response.content)
        self.assertEqual(response_json['status'], plugin.pretty_status())


class APITestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.application = ApplicationFactory()
        self.c = APIClient()
        self.token = TokenFactory(user=self.user)

    def testEntryPoint(self):
        response = self.client.post('/oauth/access_token/',
                                    {'grant_type': 'client_credentials', 'client_id': self.application.client_id,
                                     'client_secret': self.application.client_secret})
        # print response.content
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.get('/api/', {}, format='json')
        response_json = json.loads(response.content)
        self.assertEqual(response_json[0], "v3")

    def testVersionEntryPoint(self):
        response = self.client.post('/oauth/access_token/',
                                    {'grant_type': 'client_credentials', 'client_id': self.application.client_id,
                                     'client_secret': self.application.client_secret})
        # print response.content
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.get('/api/v3/', {}, format='json')
        response_json = json.loads(response.content)
        # regex_http_ports = "(:(([0-9])|([1-9][0-9])|([1-9][0-9][0-9])|([1-9][0-9][0-9][0-9])|([1-5][0-9][0-9][0-9]" \
        #                    "[0-9])|(6[0-4][0-9][0-9][0-9])|(65[0-4][0-9][0-9])|(655[0-2][0-9])|(6553[0-5])))?"
        # regex_text_http_host = "http(s)?://(\w+)(\.\w+)?" + regex_http_ports
        # regex_uri = regex_text_http_host + "/api/v3/auth/discover(/)?"
        # self.assertRegexpMatches(response_json['auth.discover'], r"^" + regex_uri + "$")

        auth_discover = ""
        if isinstance(response_json['auth.discover'], basestring):
            auth_discover = [part for part in response_json['auth.discover'].split('/') if part != ""]
            if len(auth_discover) > 2:
                auth_discover = '/'.join(auth_discover[2:])
        self.assertEqual(auth_discover, "api/v3/auth/discover")
        self.assertEqual(response.status_code, 200)
