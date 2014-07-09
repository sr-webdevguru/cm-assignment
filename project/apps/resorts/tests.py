import datetime
import json
from datetime import timedelta

from django.utils import timezone
from rest_framework.test import APITestCase, APIClient

from apps.authentication.factory.oauth_factory import ApplicationFactory, TokenFactory
from apps.custom_user.factory.user_factory import UserFactory, UserRolesFactory
from apps.resorts.factory.resort_factory import IncidentTemplateFactory, ResortFactory, UserResortMapFactory
from apps.routing.factory.routing_factory import DomainFactory


class ResortsTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory(is_admin=True)
        self.solo_user = UserFactory(email='user_solo0@admin.com', name="userSolo",
                                     user_connected=0)  # user_connected = SOLO
        self.application = ApplicationFactory()
        self.incidentTemplate = IncidentTemplateFactory(template_id=1)
        self.domain = DomainFactory(domain_id=1)
        self.domain = DomainFactory(domain_id=2, domain='api-dev-au.medic52.com', is_active=True)
        self.domain = DomainFactory(domain='testserver', is_active=True)
        self.license_expiry_date = timezone.now() + datetime.timedelta(days=2)
        self.resort = ResortFactory(domain_id=self.domain, resort_name='Vanilla Ski',
                                    license_expiry_date=self.license_expiry_date.isoformat(),
                                    licenses="2")
        self.resort1 = ResortFactory(domain_id=self.domain, resort_name='Vanilla Ski 1356', network_key="tYm6zUiK")
        self.userRoles = UserRolesFactory(role_id=1)
        self.userRoles = UserRolesFactory(role_id=2, key='dispatcher', order=2)
        self.userRoles = UserRolesFactory(role_id=3, key='manager', order=3)
        self.user_resort_map = UserResortMapFactory(role_id=3, user=self.user, resort=self.resort)
        self.user_resort_map = UserResortMapFactory(role_id=3, user=self.solo_user, resort=self.resort1)
        self.c = APIClient()
        self.token = TokenFactory(user=self.user)

    def testMobileConfig(self):
        # print self.domain.pk
        response = self.client.post('/oauth/access_token/',
                                    {'grant_type': 'client_credentials', 'client_id': self.application.client_id,
                                     'client_secret': self.application.client_secret})
        # print response.content
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')
        response = self.c.patch('/api/v3/incidents/config/?resort_id=%s' % self.resort.resort_id, {"items": []},
                                format='json')
        self.assertEqual(response.status_code, 200)
        response = self.c.get('/api/v3/incidents/config/', {"resort_id": self.resort.resort_id}, format='json')
        self.assertEqual(response.status_code, 200)

    def testMobileConfigResortNotProvided(self):
        # print self.domain.pk
        response = self.client.post('/oauth/access_token/',
                                    {'grant_type': 'client_credentials', 'client_id': self.application.client_id,
                                     'client_secret': self.application.client_secret})
        # print response.content
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')
        response = self.c.patch('/api/v3/incidents/config/', {"items": []}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['detail'], "resort_id_not_provided")
        response = self.c.get('/api/v3/incidents/config/', {"resort_id": ""}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['detail'], "resort_id_not_provided")

    def testMobileConfigInvalidUUID(self):
        # print self.domain.pk
        response = self.client.post('/oauth/access_token/',
                                    {'grant_type': 'client_credentials', 'client_id': self.application.client_id,
                                     'client_secret': self.application.client_secret})
        # print response.content
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')
        response = self.c.patch('/api/v3/incidents/config/?resort_id=%s' % "aaa", {"items": []}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['detail'], "not_a_valid_uuid")
        response = self.c.get('/api/v3/incidents/config/', {"resort_id": "aaa"}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['detail'], "not_a_valid_uuid")

    def testMobileConfigNotExist(self):
        # print self.domain.pk
        response = self.client.post('/oauth/access_token/',
                                    {'grant_type': 'client_credentials', 'client_id': self.application.client_id,
                                     'client_secret': self.application.client_secret})
        # print response.content
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')
        response = self.c.get('/api/v3/incidents/config/', {"resort_id": str(self.user.user_id)}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['detail'], "resort_does_not_exists")
        response = self.c.patch('/api/v3/incidents/config/?resort_id=%s' % str(self.user.user_id), {"items": []},
                                format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['detail'], "resort_does_not_exists")

    def testMobileConfigUserConnected0(self):
        # print self.domain.pk
        response = self.client.post('/oauth/access_token/',
                                    {'grant_type': 'client_credentials', 'client_id': self.application.client_id,
                                     'client_secret': self.application.client_secret})
        # print response.content
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.solo_user.email, 'password': '1234'},
                               format='json')
        response = self.c.get('/api/v3/incidents/config/', {"resort_id": self.resort1.resort_id}, format='json')
        self.assertEqual(response.status_code, 200)

    def testResortExpiry(self):
        # test Create User with resort license expire
        response = self.client.post('/oauth/access_token/',
                                    {'grant_type': 'client_credentials', 'client_id': self.application.client_id,
                                     'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')

        # create user with resort license expire
        response = self.c.post('/api/v3/users/',
                               {
                                   "name": "Mr Duncan",
                                   "email": "manager@summit.com",
                                   "password": "SuperSimple2015",
                                   "phone": "0138562894",
                                   "role_id": 1,
                                   "resort_id": str(self.resort.resort_id),
                                   "status": "Active",
                                   "resort_network_key": self.resort.network_key
                               }, format='json')
        # print response
        self.assertEqual(response.status_code, 200)

        # udpate resort license to expire
        self.license_expiry_date -= timedelta(days=2)
        response = self.c.put('/api/v3/resorts/' + str(self.resort.resort_id) + '/',
                              {
                                  "license_expiry_date": self.license_expiry_date.isoformat()
                              }, format='json')

        # test Register with resort license expire
        response = self.c.post('/api/v3/auth/register/',
                               {
                                   "name": "Mr Roberts",
                                   "email": "manager@vanillaski.com",
                                   "resort_name": "Vanilla Ski",
                                   "device_push_token": "3a0c0ac71ee49eac8b0444a85f1c16692106c3d3bc50d17f8bd79e4a7a0f538",
                                   "device_os": "iOS 7.0.2",
                                   "device_type": "iPhone 6",
                                   "country": "United States",
                                   "timezone": "Australia/Sydney",
                                   "password": "SuperSimple2015",
                                   "role": 3,
                                   "resort_id": self.resort.resort_id,
                                   "resort_network_key": self.resort.network_key
                               }, format='json')
        # print response
        self.assertEqual(response.data['detail'], 'resort_expiry_date_past')

        # test Login with resort license expire
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/',
                               {
                                   'email': 'duncan@sixfive.com',
                                   'password': '1234'
                               }, format='json')
        # print response
        self.assertEqual(response.data['detail'], 'resort_expiry_date_past')

    def testResortsMaximumUsers(self):
        # test Register with resort maximum license users (1st User)
        response = self.client.post('/oauth/access_token/',
                                    {'grant_type': 'client_credentials', 'client_id': self.application.client_id,
                                     'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = self.c.post('/api/v3/auth/register/',
                               {
                                   "name": "Mr Roberts",
                                   "email": "manager@vanillaski.com",
                                   "resort_name": "Vanilla Ski",
                                   "device_push_token": "3a0c0ac71ee49eac8b0444a85f1c16692106c3d3bc50d17f8bd79e4a7a0f538",
                                   "device_os": "iOS 7.0.2",
                                   "device_type": "iPhone 6",
                                   "country": "United States",
                                   "timezone": "Australia/Sydney",
                                   "password": "SuperSimple2015",
                                   "role": 3,
                                   "resort_network_key": str(self.resort.network_key)
                               }, format='json')
        # print response
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.data['detail'], 'no_more_licenses')

        # test Create User with resort maximum license users (2nd User which must not be created since maximum license of resort is 1)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')

        # udpate resort number of license
        response = self.c.put('/api/v3/resorts/' + str(self.resort.resort_id) + '/',
                              {
                                  "licenses": "1"
                              }, format='json')
        # print response

        response = self.c.post('/api/v3/users/',
                               {
                                   "name": "Mr Duncan",
                                   "email": "manager@summit.com",
                                   "password": "SuperSimple2015",
                                   "phone": "0138562894",
                                   "role_id": 1,
                                   "resort_id": str(self.resort.resort_id),
                                   "status": "Active",
                                   "resort_network_key": str(self.resort.network_key)
                               }, format='json')
        # print response
        self.assertEqual(response.data['detail'], 'no_more_licenses')

        # check added users network connected
        # self.users = Users.objects.all()
        # for user in self.users:
        #    print user.name, user.email, user.user_connected
        # print Users.objects.get(pk=1), "debug"
