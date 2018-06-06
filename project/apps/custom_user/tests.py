import json

from rest_framework.test import APITestCase, APIClient

from apps.authentication.factory.oauth_factory import ApplicationFactory
from apps.authentication.factory.oauth_factory import TokenFactory
from apps.custom_user.factory.user_factory import UserFactory
from apps.custom_user.factory.user_factory import UserRolesFactory
from apps.resorts.factory.resort_factory import IncidentTemplateFactory, ResortFactory, UserResortMapFactory
from apps.routing.factory.routing_factory import DomainFactory
from apps.routing.models import Domains


class RegisterTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.application = ApplicationFactory()
        # Clear ALL existing Domains
        Domains.objects.all().delete()
        self.domain = DomainFactory(__sequence=1, domain='api-dev-us.medic52.com')
        self.domain = DomainFactory(domain_id=2, domain='api-dev-au.medic52.com', is_active=True)
        self.domain = DomainFactory(domain='testserver', is_active=True)
        self.domain = DomainFactory(domain='localhost', is_active=True)
        self.incidentTemplate = IncidentTemplateFactory(template_id=1)
        self.resort = ResortFactory(domain_id=self.domain, resort_name='Vanilla Ski',
                                    license_expiry_date='2018-04-01T00:00:00', licenses=5)
        self.userRoles = UserRolesFactory(role_id=1)
        self.userRolesDispatcher = UserRolesFactory(role_id=2, key='dispatcher', order=2)
        self.userRolesManager = UserRolesFactory(role_id=3, key='manager', order=3)
        self.user_resort_map = UserResortMapFactory(role_id=self.userRolesDispatcher.role_id, user=self.user,
                                                    resort=self.resort)
        self.c = APIClient()
        self.token = TokenFactory(user=self.user)

    def testMobileRegister(self):
        # test invalid_token_header_no_access_token_provided
        # print self.domain.pk
        response = self.client.post('/oauth/access_token/',
                                    {'grant_type': 'client_credentials', 'client_id': self.application.client_id,
                                     'client_secret': self.application.client_secret})
        # print response.content
        self.access_token = json.loads(response.content)['access_token']
        # self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')
        response = self.c.post('/api/v3/auth/register/', {"name": "Mr Roberts",
                                                          "email": "manager@vanillaski.com",
                                                          "resort_name": "Vanilla Ski",
                                                          "device_push_token": "3a0c0ac71ee49eac8b0444a85f1c16692106c3d3bc50d17f8bd79e4a7a0f538",
                                                          "device_os": "iOS 7.0.2",
                                                          "device_type": "iPhone 6",
                                                          "country": "United States",
                                                          "timezone": "Australia/Sydney",
                                                          "password": "SuperSimple2015"}, format='json')
        self.assertEqual(response.status_code, 401)

        # test resort_with_network_key_does_not_exist
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')
        response = self.c.post('/api/v3/auth/register/', {"name": "Mr Roberts",
                                                          "email": "manager@vanillaski.com",
                                                          "resort_name": "Toggenburg",
                                                          "device_push_token": "3a0c0ac71ee49eac8b0444a85f1c16692106c3d3bc50d17f8bd79e4a7a0f538",
                                                          "device_os": "iOS 7.0.2",
                                                          "device_type": "iPhone 6",
                                                          "country": "United States",
                                                          "timezone": "Australia/Sydney",
                                                          "password": "SuperSimple2015",
                                                          "resort_network_key": "ZmY4YzZmx"}, format='json')
        # print response
        self.assertEqual(response.status_code, 400)

        # Success register
        response = self.c.post('/api/v3/auth/register/', {"name": "Mr Roberts",
                                                          "email": "manager@vanillaski.com",
                                                          "resort_name": "Toggenburg",
                                                          "device_push_token": "3a0c0ac71ee49eac8b0444a85f1c16692106c3d3bc50d17f8bd79e4a7a0f538",
                                                          "device_os": "iOS 7.0.2",
                                                          "device_type": "iPhone 6",
                                                          "country": "Australia",
                                                          "timezone": "Australia/Sydney",
                                                          "password": "SuperSimple2015"}, format='json')
        self.assertEqual(response.status_code, 200)

    def testMobileRegisterUSDomainFromAustralia(self):
        response = self.client.post('/oauth/access_token/',
                                    {'grant_type': 'client_credentials', 'client_id': self.application.client_id,
                                     'client_secret': self.application.client_secret})
        # print response.content
        self.access_token = json.loads(response.content)['access_token']

        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')
        with self.settings(RUN_ENV='test'):
            response = self.c.post('/api/v3/auth/register/', {"name": "Mr Roberts",
                                                              "email": "manager@vanillaski.com",
                                                              "resort_name": "Toggenburg",
                                                              "device_push_token": "3a0c0ac71ee49eac8b0444a85f1c16692106c3d3bc50d17f8bd79e4a7a0f538",
                                                              "device_os": "iOS 7.0.2",
                                                              "device_type": "iPhone 6",
                                                              "country": "Australia",
                                                              "timezone": "Australia/Sydney",
                                                              "password": "SuperSimple2015"}, format='json',
                                   HTTP_HOST='api-dev-us.medic52.com')
            self.assertEqual(response.status_code, 200)

    def testMobileRegisterAUDomainFromUSA(self):
        response = self.client.post('/oauth/access_token/',
                                    {'grant_type': 'client_credentials', 'client_id': self.application.client_id,
                                     'client_secret': self.application.client_secret})
        # print response.content
        self.access_token = json.loads(response.content)['access_token']

        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')
        with self.settings(RUN_ENV='test'):
            response = self.c.post('/api/v3/auth/register/', {"name": "Mr Roberts",
                                                              "email": "manager1@vanillaski1.com",
                                                              "resort_name": "Toggenburg",
                                                              "device_push_token": "3a0c0ac71ee49eac8b0444a85f1c16692106c3d3bc50d17f8bd79e4a7a0f538",
                                                              "device_os": "iOS 7.0.2",
                                                              "device_type": "iPhone 6",
                                                              "country": "United States",
                                                              "timezone": "Australia/Sydney",
                                                              "password": "SuperSimple2015"}, format='json',
                                   HTTP_HOST='api-dev-au.medic52.com')
            self.assertEqual(response.status_code, 200)


class RolesUserTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.application = ApplicationFactory()
        self.userRoles = UserRolesFactory(role_id=1, key='patroller', order=1)
        self.userRoles = UserRolesFactory(role_id=2, key='dispatcher', order=2)
        self.userRoles = UserRolesFactory(role_id=3, key='manager', order=3)
        self.incidentTemplate = IncidentTemplateFactory(template_id=1)
        self.domain4 = DomainFactory(domain='localhost', is_active=True)
        self.resort = ResortFactory(domain_id=self.domain4, resort_name='Vanilla Ski',
                                    license_expiry_date='2018-04-01T00:00:00', licenses=5)
        self.user_resort_map = UserResortMapFactory(role_id=self.userRoles.role_id, user=self.user, resort=self.resort)
        self.c = APIClient()

    def testMobileGet(self):
        response = self.client.post('/oauth/access_token/',
                                    {'grant_type': 'client_credentials', 'client_id': self.application.client_id,
                                     'client_secret': self.application.client_secret})
        # print response.content
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')
        response = self.c.get('/api/v3/users/roles/', {}, format='json')
        response_json = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertGreater(response_json['count'], 0, "No Roles in response")


class UserViewSetTestCase(APITestCase):
    """
    Purpose - Test Case for UserViewSet API methods.
    Date created - 07/07/2015
    Date updated - 08/30/2015
    Updates made:
     - Fix ordering user list.
    command:
     - python manage.py test apps.custom_user.tests.UserViewSetTestCase
    """

    def setUp(self):
        self.user = UserFactory(email='aname@testing.com', name='aname', is_admin=True)
        self.other_user = UserFactory(email='bname@testing.com', name='bname', is_admin=False)

        # Users for list tests:

        self.userc = UserFactory(email='cname@testing.com', name='cname')
        self.userd = UserFactory(email='dname@testing.com', name='dname')
        self.usere = UserFactory(email='ename@testing.com', name='ename')
        self.userf = UserFactory(email='fname@testing.com', name='fname')
        self.userg = UserFactory(email='gname@testing.com', name='gname')
        self.userh = UserFactory(email='hname@testing.com', name='hname')
        self.useri = UserFactory(email='iname@testing.com', name='iname')
        self.userj = UserFactory(email='jname@testing.com', name='jname')
        self.userk = UserFactory(email='kname@testing.com', name='kname')

        self.application = ApplicationFactory()
        # self.domain = DomainFactory(domain = 'testing.com', is_active = True)
        self.domain = DomainFactory(domain_id=1, is_active=True)
        self.incidentTemplate = IncidentTemplateFactory(template_id=1)
        self.resort = ResortFactory(domain_id=self.domain, resort_name='Vanilla Ski 1',
                                    license_expiry_date='2018-04-01T00:00:00', licenses=5)
        self.other_resort = ResortFactory(domain_id=self.domain, resort_name='Toggenburg', network_key="4520ce8",
                                          license_expiry_date='2018-04-01T00:00:00', licenses=5)
        self.userRoles = UserRolesFactory(role_id=1, key='patroller', order=1)
        self.userRoles = UserRolesFactory(role_id=2, key='dispatcher', order=2)
        self.userRoles = UserRolesFactory(role_id=3, key='manager', order=3)
        self.user_resort_map = UserResortMapFactory(role_id=3, user=self.user, resort=self.resort)
        self.other_user_resort_map = UserResortMapFactory(role_id=3, user=self.other_user, resort=self.other_resort)
        self.user_resort_map = UserResortMapFactory(role_id=3, user=self.userc, resort=self.resort)
        self.user_resort_map = UserResortMapFactory(role_id=3, user=self.userd, resort=self.resort)
        self.user_resort_map = UserResortMapFactory(role_id=2, user=self.usere, resort=self.resort)
        self.user_resort_map = UserResortMapFactory(role_id=2, user=self.userf, resort=self.resort)
        self.user_resort_map = UserResortMapFactory(role_id=2, user=self.userg, resort=self.resort)
        self.user_resort_map = UserResortMapFactory(role_id=1, user=self.userh, resort=self.resort)
        self.user_resort_map = UserResortMapFactory(role_id=1, user=self.useri, resort=self.resort)
        self.user_resort_map = UserResortMapFactory(role_id=1, user=self.userj, resort=self.resort)
        self.user_resort_map = UserResortMapFactory(role_id=1, user=self.userk, resort=self.resort)
        self.c = APIClient()
        self.token = TokenFactory(user=self.user)

    def testMobileCreate(self):
        """
        Purpose - Test Case for UserViewSet API create method.
        Date created - 07/07/2015
        Date updated - 08/30/2015
        Updates made:
         - 
        command:
         - python manage.py test apps.custom_user.tests.UserViewSetTestCase.testMobileCreate
        """

        response = self.client.post('/oauth/access_token/',
                                    {'grant_type': 'client_credentials', 'client_id': self.application.client_id,
                                     'client_secret': self.application.client_secret})
        # print response.content
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')
        create_user_response = self.c.post('/api/v3/users/', {
            "name": "Mr New User",
            "email": "testing_new_user@testing.com",
            "password": "SuperSimple2015",
            "phone": "013262894",
            "role_id": 1,
            "resort_id": self.resort.resort_id,
            "status": "Active"
        }, format='json')
        self.assertEqual(create_user_response.status_code, 200)

    def testMobileGet(self):
        """
        Purpose - Test Case for UserViewSet API get method.
        Date created - 07/07/2015
        Date updated - 08/30/2015
        Updates made:
         - 
        command:
         - python manage.py test apps.custom_user.tests.UserViewSetTestCase.testMobileGet
        """

        response = self.client.post('/oauth/access_token/',
                                    {'grant_type': 'client_credentials', 'client_id': self.application.client_id,
                                     'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')
        new_user_url = '/api/v3/users/' + json.loads(response.content)['user']['user_id'] + '/'
        get_user_response = self.c.get(new_user_url)
        self.assertEqual(get_user_response.status_code, 200)

    def testMobileDevices(self):
        """
        Purpose - Test Case for UserViewSet API get devices method.
        Date created - 07/07/2015
        Date updated - 08/30/2015
        Updates made:
         - 
        command:
         - python manage.py test apps.custom_user.tests.UserViewSetTestCase.testMobileDevices
        """

        response = self.client.post('/oauth/access_token/',
                                    {'grant_type': 'client_credentials', 'client_id': self.application.client_id,
                                     'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')
        new_user_url = '/api/v3/users/' + json.loads(response.content)['user']['user_id'] + '/devices/'
        get_user_response = self.c.get(new_user_url)
        self.assertEqual(get_user_response.status_code, 200)

    def testUserListAndSorting(self):
        """
        Purpose - Test Case for UserViewSet API list method.
        Date created - 07/07/2015
        Date updated - 08/30/2015
        Updates made:
         - 
        command:
         - python manage.py test apps.custom_user.tests.UserViewSetTestCase.testUserListAndSorting
        """

        response = self.client.post('/oauth/access_token/',
                                    {'grant_type': 'client_credentials', 'client_id': self.application.client_id,
                                     'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')
        get_user_response = self.c.get('/api/v3/users/')
        self.assertEqual(get_user_response.status_code, 200)

        get_users_sorted_response = self.c.get('/api/v3/users/?offset=0&chunk=4&order_by=name&order_by_direction=asc')
        self.assertEqual(get_users_sorted_response.status_code, 200)

        sorted_list = json.loads(get_users_sorted_response.content)['results']

        # Chunk of first 4 users sorted by name ASC
        self.assertEqual(sorted_list[0]['name'], "bname")
        self.assertEqual(sorted_list[1]['name'], "cname")
        self.assertEqual(sorted_list[2]['name'], "dname")
        self.assertEqual(sorted_list[3]['name'], "ename")

        get_users_sorted_response = self.c.get('/api/v3/users/?offset=0&chunk=4&order_by=name&order_by_direction=desc')
        self.assertEqual(get_users_sorted_response.status_code, 200)

        sorted_list = json.loads(get_users_sorted_response.content)['results']

        # Chunk of first 4 users sorted by name DESC
        self.assertEqual(sorted_list[0]['name'], "kname")
        self.assertEqual(sorted_list[1]['name'], "jname")
        self.assertEqual(sorted_list[2]['name'], "iname")
        self.assertEqual(sorted_list[3]['name'], "hname")
        """
        get_users_sorted_response = self.c.get('/api/v3/users/?offset=0&chunk=6&order_by=role_id&order_by_direction=asc')
        self.assertEqual(get_users_sorted_response.status_code, 200)
        
        sorted_list = json.loads(get_users_sorted_response.content)['results']
        
        #Chunk of first 6 users sorted by role_id ASC
        self.assertEqual(sorted_list[0]['role_id']['value'], 1)
        self.assertEqual(sorted_list[1]['role_id']['value'], 1)
        self.assertEqual(sorted_list[2]['role_id']['value'], 1)
        self.assertEqual(sorted_list[3]['role_id']['value'], 1)
        self.assertEqual(sorted_list[4]['role_id']['value'], 2)
        self.assertEqual(sorted_list[5]['role_id']['value'], 2)
        
        get_users_sorted_response = self.c.get('/api/v3/users/?offset=0&chunk=6&order_by=role_id&order_by_direction=desc')
        self.assertEqual(get_users_sorted_response.status_code, 200)
        
        sorted_list = json.loads(get_users_sorted_response.content)['results']
        
        #Chunk of first 6 users sorted by role_id DESC
        self.assertEqual(sorted_list[0]['role_id']['value'], 3)
        self.assertEqual(sorted_list[1]['role_id']['value'], 3)
        self.assertEqual(sorted_list[2]['role_id']['value'], 3)
        self.assertEqual(sorted_list[3]['role_id']['value'], 3)
        self.assertEqual(sorted_list[4]['role_id']['value'], 2)
        self.assertEqual(sorted_list[5]['role_id']['value'], 2)
        """

    def testMobileListAsManager(self):
        """
        Purpose - Test Case for UserViewSet API list method as Manager.
        Date created - 07/07/2015
        Date updated - 08/30/2015
        Updates made:
         - 
        command:
         - python manage.py test apps.custom_user.tests.UserViewSetTestCase.testMobileListAsManager
        """

        response = self.client.post('/oauth/access_token/',
                                    {'grant_type': 'client_credentials', 'client_id': self.application.client_id,
                                     'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.other_user.email, 'password': '1234'},
                               format='json')
        get_user_response = self.c.get('/api/v3/users/')
        self.assertEqual(get_user_response.status_code, 200)

    def testMobileUpdate(self):
        """
        Purpose - Test Case for UserViewSet API update method.
        Date created - 07/07/2015
        Date updated - 08/30/2015
        Updates made:
         - 
        command:
         - python manage.py test apps.custom_user.tests.UserViewSetTestCase.testMobileUpdate
        """

        response = self.client.post('/oauth/access_token/',
                                    {'grant_type': 'client_credentials', 'client_id': self.application.client_id,
                                     'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')
        new_user_url = '/api/v3/users/' + str(self.user.user_id).encode("utf8") + '/'

        # Test Update
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')
        update_user_response = self.c.put(new_user_url, {
            "name": "Mr New User 2",
            "email": self.user.email,
            "role_id": 2,
            "status": "Active"
        }, format='json')
        # print update_user_response
        self.assertEqual(update_user_response.status_code, 200)

    def testMobileDestroy(self):
        """
        Purpose - Test Case for UserViewSet API destroy method.
        Date created - 07/07/2015
        Date updated - 08/30/2015
        Updates made:
         - 
        command:
         - python manage.py test apps.custom_user.tests.UserViewSetTestCase.testMobileDestroy
        """

        response = self.client.post('/oauth/access_token/',
                                    {'grant_type': 'client_credentials', 'client_id': self.application.client_id,
                                     'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')
        new_user_url = '/api/v3/users/' + json.loads(response.content)['user']['user_id'] + '/'
        get_user_response = self.c.delete(new_user_url)
        self.assertEqual(get_user_response.status_code, 200)

    def testUpdateCreateUser(self):
        """
        Purpose - Test Case for UserViewSet API update and create method.
        Date created - 07/07/2015
        Date updated - 08/30/2015
        Updates made:
         - 
        command:
         - python manage.py test apps.custom_user.tests.UserViewSetTestCase.testUpdateCreateUser
        """
        # 272 Test User Update/Create API
        # 1. Manager user can update users within the same resort
        response = self.client.post('/oauth/access_token/',
                                    {'grant_type': 'client_credentials', 'client_id': self.application.client_id,
                                     'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')
        # create user using manager account
        response = self.c.post('/api/v3/users/',
                               {
                                   "name": "Mr Patroller",
                                   "email": "patroller@summit.com",
                                   "password": "SuperSimple2015",
                                   "phone": "0138562894",
                                   "role_id": 1,
                                   "resort_id": str(self.resort.resort_id),
                                   "status": "Active"
                               }, format='json')
        # print response
        self.assertEqual(response.status_code, 200)

        # update user using manager account
        # print response.data
        user_id = response.data['user_id']
        response = self.c.put('/api/v3/users/' + user_id + '/',
                              {
                                  "name": "Mr Patroller Edited by Manager",
                                  "email": "patroller@summit.com"
                              }, format='json')

        # print response
        self.assertEqual(response.status_code, 200)

        # 2. Patroller & Dispatcher users can only edit their own accounts
        # update Patroller User using Patroller own acccount
        response = self.c.post('/api/v3/auth/login/', {'email': "patroller@summit.com", 'password': 'SuperSimple2015'},
                               format='json')
        response = self.c.put('/api/v3/users/' + user_id + '/',
                              {
                                  "name": "Mr Patroller Edited by Patroller own account",
                                  "email": "patroller@summit.com"
                              }, format='json')
        # print response
        self.assertEqual(response.status_code, 200)

        # create dispatcher user by manager
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')
        # create user
        response = self.c.post('/api/v3/users/',
                               {
                                   "name": "Mr Dispatcher",
                                   "email": "dispatcher@summit.com",
                                   "password": "SuperSimple2015",
                                   "phone": "0138562894",
                                   "role_id": 2,
                                   "resort_id": str(self.resort.resort_id),
                                   "status": "Active"
                               }, format='json')
        # print response
        self.assertEqual(response.status_code, 200)

        # update Dispatcher User using Dispatcher own account
        user_id = response.data['user_id']
        response = self.c.post('/api/v3/auth/login/', {'email': "dispatcher@summit.com", 'password': 'SuperSimple2015'},
                               format='json')
        response = self.c.put('/api/v3/users/' + user_id + '/',
                              {
                                  "name": "Mr Dispatcher Edited by Dispatcher own account",
                                  "email": "dispatcher@summit.com"
                              }, format='json')
        # print response
        self.assertEqual(response.status_code, 200)

        # 3. No one should be able to update a user outside their own resort.
        # update Dispatcher User from other resort Manager
        user_id = response.data['user_id']
        response = self.c.post('/api/v3/auth/login/', {'email': self.other_user.email, 'password': '1234'},
                               format='json')
        response = self.c.put('/api/v3/users/' + user_id + '/',
                              {
                                  "name": "Mr Dispatcher Edited by Manager outside account",
                                  "email": "dispatcher@summit.com"
                              }, format='json')
        # print response
        self.assertEqual(response.data['detail'], "You don't have permission to update user")

        # 4. Only Manager can create / delete users, and only within their own resort
        response = self.c.post('/api/v3/auth/login/', {'email': self.other_user.email, 'password': '1234'},
                               format='json')
        response = self.c.delete('/api/v3/users/' + user_id + '/')
        # print response
        self.assertEqual(response.data['detail'], 'you_dont_have_permission_to_delete_user')
        # self.assertEqual(response.status_code, 200)

        # for user in UserResortMap.objects.all():
        #    print user.user.user_id, user.user.name, user.user.email, user.role_id
