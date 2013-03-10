import json

from django.utils import timezone
from rest_framework.test import APITestCase, APIClient

from apps.authentication.factory.oauth_factory import ApplicationFactory
from apps.authentication.factory.oauth_factory import TokenFactory
from apps.custom_user.factory.user_factory import UserFactory
from apps.custom_user.factory.user_factory import UserRolesFactory
from apps.data_sync.factory.data_sync_factory import LanguageFactory
from apps.incidents.factory.incident_factory import IncidentStatusFactory
from apps.resorts.factory.resort_factory import IncidentTemplateFactory, ResortFactory, UserResortMapFactory
from apps.routing.factory.routing_factory import DomainFactory

incident_json = {
    "field_52d47a654d1bb": "Gary Barlow",
    "field_52d47a654d1cc": 2,
    "field_52d47a654d1dd": "garry@barrlow.com",
    "field_52d47a654d1ee": "1978-07-15",
    "field_52d47a654d1ff": "male",
    "field_52ca456962ba8": {
        "lat": -150.3456787,
        "long": 33.0639757,
        "accuracy": 5
    },
    "field_52d47a654d1aa": [
        {
            "field_52d47a654d11a": "reftophoto1",
            "field_52d47a654d121": "2015-02-15 21:09:52"
        },
        {
            "field_52d47a654d11a": "reftophoto2",
            "field_52d47a654d121": "2015-02-15 21:09:59"
        }
    ],
    "field_52d47b5fdda86": [
        {
            "field_52d47a654d141": "Mr Witness Name",
            "field_52d47a654d142": "1960-02-27",
            "field_52d47a654d143": 79,
            "field_52d47a654d144": "reftoaudiostatement1",
            "field_52d47a654d145": "2015-02-15 21:12:03"
        }
    ],
    "field_52dd8c049b005": 96,
    "field_52dd8bee9b004": 198,
    "field_52ca429c62b98": "yes",
    "field_52d483dceb786": [
        204,
        206,
        212
    ],
    "field_52ca430462b9a": "yes",
    "field_52dd8a57e95a7": "POC",
    "field_54b084fb2d255": "no",
    "field_52ca3fcc59d29": "no",
    "field_52d4767cde30d": [
        {
            "field_52d47a654d1fb": 5,
            "field_52d47a654d1fc": 4,
            "field_52d47a654d1fd": 3,
            "field_52d47a654d1ef": 40,
            "field_52d47a654d1ee": 120,
            "field_52d47a654d1ed": 98,
            "field_52d47a654d1ec": "22/80",
            "field_52d47a654d1eb": 5,
            "field_52d47a654d1ea": "2015-02-15 21:12:03"
        },
        {
            "field_52d47a654d1fb": 5,
            "field_52d47a654d1fc": 4,
            "field_52d47a654d1fd": 3,
            "field_52d47a654d1ef": 38,
            "field_52d47a654d1ee": 110,
            "field_52d47a654d1ed": 98,
            "field_52d47a654d1ec": "40/80",
            "field_52d47a654d1eb": 4,
            "field_52d47a654d1ea": "2015-02-15 21:16:55"
        },
        {
            "field_52d47a654d1fb": 5,
            "field_52d47a654d1fc": 4,
            "field_52d47a654d1fd": 3,
            "field_52d47a654d1ef": 40,
            "field_52d47a654d1ee": 120,
            "field_52d47a654d1ed": 98,
            "field_52d47a654d1ec": "22/80",
            "field_52d47a654d1eb": 3,
            "field_52d47a654d1ea": "2015-02-15 21:21:28"
        }
    ],
    "field_52d4798f6d229": [
        {
            "field_52d47a654d2aa": 152,
            "field_52d47a654d2ab": 129,
            "field_52d47a654d2ac": 166,
            "field_52d47a654d2ad": 234
        }
    ],
    "field_52ca445d62ba1": [
        22,
        25,
        29
    ],
    "field_52d4800164f2e": [
        {
            "field_52ca445d62ba2": 31,
            "field_52ca445d62ba3": 25,
            "field_52ca445d62ba4": 527,
            "field_52ca445d62ba5": "2015-02-15 21:20:28"
        }
    ],
    "field_52d47e4cedbe2": "Plenty of patroller notes on this incident",
    "field_52d47de5edbdf": "reftosignaturefile1",
    "notes": [
        {
            "note_id": 234,
            "note_by": 4225,
            "note_date": "2015-02-15 21:45:03",
            "note": "Helicopter called via EMS dispatch"
        }
    ]
}


class DeviceTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.inactive_user = UserFactory(email='jerol@lycos.com', name='Duncan', is_active=False)
        self.userPatroller = UserFactory(email='patroller@yahoo.com', name='Mr Patroller',
                                         user_connected=1, is_active=True)
        self.userPatroller2 = UserFactory(email='patroller2@yahoo.com', name='Mr Patroller2',
                                          user_connected=1, is_active=True)
        self.userDispatcher = UserFactory(email='dispatcher@yahoo.com', name='Mr Dispatcher',
                                          user_connected=1, is_active=True)
        self.userDispatcher2 = UserFactory(email='dispatcher2@yahoo.com', name='Mr Dispatcher2',
                                           user_connected=1, is_active=True)
        self.language = LanguageFactory()
        self.domain = DomainFactory(domain_id=1)
        self.incidentTemplate = IncidentTemplateFactory(template_id=1)
        self.resort = ResortFactory(domain_id=self.domain)
        self.userRolePatroller = UserRolesFactory(role_id=1, key='patroller', order=1)
        self.userRoleDispatcher = UserRolesFactory(role_id=2, key='dispatcher', order=2)
        self.userRoleManager = UserRolesFactory(role_id=3, key='manager', order=3)
        self.userResortMapPatroller = UserResortMapFactory(role_id=self.userRolePatroller.role_id,
                                                           user=self.userPatroller, resort=self.resort)
        self.userResortMapPatroller2 = UserResortMapFactory(role_id=self.userRolePatroller.role_id,
                                                            user=self.userPatroller2, resort=self.resort)
        self.userResortMapDispatcher = UserResortMapFactory(role_id=self.userRoleDispatcher.role_id,
                                                            user=self.userDispatcher, resort=self.resort)
        self.userResortMapDispatcher2 = UserResortMapFactory(role_id=self.userRoleDispatcher.role_id,
                                                             user=self.userDispatcher2, resort=self.resort)
        self.userResortMapManager = UserResortMapFactory(role_id=self.userRoleManager.role_id,
                                                         user=self.user, resort=self.resort)
        self.incidentStatus = IncidentStatusFactory(incident_status_id=1)
        self.application = ApplicationFactory()
        self.c = APIClient()
        self.token = TokenFactory(user=self.user)

    def testMobileHeartbeat(self):
        # print self.domain.pk
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        # print response.content
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')
        response = self.c.get('/api/v3/devices/bc105f7c-cdf2-4ab8-b0d9-8710259b3991/heartbeat/',
                              {"resort_id": "8819368a-9824-416e-a8b3-367159e0775f",
                               "user_id": "9704b80d-cd29-43ea-95be-eb4809803b4b"}, format='json')
        self.assertEqual(response.status_code, 400)

    def testMobileCreateDevice(self):
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')

        # User inactive or deleted.
        response = self.c.post('/api/v3/devices/',
                               {"device_push_token": "3a0c0ac71ee49eac8b0444a85f1c16692106c3d3bc50d17f8bd",
                                "device_os": "iOS 7.0.2",
                                "device_type": "iPhone 6",
                                "device_connected": 0,
                                "user_id": self.inactive_user.user_id}, format='json')
        self.assertEqual(response.status_code, 403)

        # successful add device
        response = self.c.post('/api/v3/devices/',
                               {"device_push_token": "3a0c0ac71ee49eac8b0444a85f1c16692106c3d3bc50d17f8bd",
                                "device_os": "iOS 7.0.2",
                                "device_type": "iPhone 6",
                                "device_connected": 0,
                                "user_id": self.user.user_id}, format='json')
        device_id = response.data['device_id']
        self.assertEqual(response.status_code, 200)

        # error add device
        response = self.c.post('/api/v3/devices/',
                               {"device_connected": 0,
                                "user_id": self.user.user_id}, format='json')
        self.assertEqual(response.status_code, 400)

        # user does not exist
        response = self.c.post('/api/v3/devices/',
                               {"device_connected": 0,
                                "user_id": "da68bad5-d966-4c2a-a648-d1ca737565ce"}, format='json')
        self.assertEqual(response.status_code, 400)

        # user is not provided
        response = self.c.post('/api/v3/devices/',
                               {"device_connected": 0}, format='json')
        self.assertEqual(response.status_code, 400)

        # Update device
        response = self.c.put('/api/v3/devices/' + str(device_id) + '/',
                              {"device_push_token": "3a0c0ac71ee49eac8b0444a85f1c16692106c3d3bc50d17f8bd",
                               "device_os": "iOS 7.0.2",
                               "device_type": "iPhone 8",
                               "device_connected": 0}, format='json')
        # print response
        self.assertEqual(response.status_code, 200)

        # Device does not exists
        response = self.c.put('/api/v3/devices/0b924268-3164-430e-ac68-8a8332b6eada/',
                              {"device_push_token": "3a0c0ac71ee49eac8b0444a85f1c16692106c3d3bc50d17f8bd",
                               "device_os": "iOS 7.0.2",
                               "device_type": "iPhone 8",
                               "device_connected": 0}, format='json')
        # print response
        self.assertEqual(response.status_code, 400)

        # Retreive device
        response = self.c.get('/api/v3/devices/' + str(device_id) + '/',
                              {}, format='json')
        # print response
        self.assertEqual(response.status_code, 200)

        # Device does not exists
        response = self.c.get('/api/v3/devices/0b924268-3164-430e-ac68-8a8332b6eada/',
                              {}, format='json')
        self.assertEqual(response.status_code, 400)

        # remote wipe device
        response = self.c.get('/api/v3/devices/' + str(device_id) + '/heartbeat/',
                              {'resort_id': self.userResortMapManager.resort.resort_id,
                               'user_id': self.userResortMapManager.user.user_id}, format='json')
        # print response
        self.assertEqual(response.status_code, 200)

    def testHeartbeatDevice(self):
        # 273 Tests heartbeat assignee
        from django.db import connection

        with connection.cursor() as c:
            c.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')

        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.userPatroller.email, 'password': '1234'},
                               format='json')
        # Patroller registers with a device via API
        response = self.c.post('/api/v3/devices/',
                               {"device_push_token": "3a0c0ac71ee49eac8b0444a85f1c16692106c3d3bc50d17f8bd",
                                "device_os": "iOS 7.0.2",
                                "device_type": "iPhone 6",
                                "device_connected": 0,
                                "user_id": self.userPatroller.user_id}, format='json')
        device_id = str(response.data['device_id'])
        self.assertEqual(response.status_code, 200)

        # Dispatch in same resort create incident and assign to that patroller
        response = self.c.post('/api/v3/auth/login/', {'email': self.userDispatcher.email, 'password': '1234'},
                               format='json')
        incident_json_initial = incident_json
        incident_json_initial['notes'][0]['note_by'] = str(self.userDispatcher.user_pk)
        response = self.c.post('/api/v3/incidents/', incident_json_initial, format='json')

        # Dispatcher update and assign to patroller
        incident_json_update = {
            "field_52d47a654d1dd": "gary@barlow.com",
            "field_52dd8a57e95a7": "Giro",
            "field_52d4767cde30d": [
                {
                    "field_52d47a654d1fb": 5,
                    "field_52d47a654d1fc": 4,
                    "field_52d47a654d1fd": 3,
                    "field_52d47a654d1ef": 40,
                    "field_52d47a654d1ee": 120,
                    "field_52d47a654d1ed": 98,
                    "field_52d47a654d1ec": "22/80",
                    "field_52d47a654d1eb": 5,
                    "field_52d47a654d1ea": "2015-02-15 21:45:03"
                }
            ],
            "assigned_to": str(self.userPatroller.user_id),
            "notes": [
                {
                    "note_by": str(self.userDispatcher.user_pk),
                    "note_date": "2015-02-15 21:45:03",
                    "note": "Helicopter called via EMS dispatch. Really"
                }
            ]
        }
        # update incident
        incident_id = str(response.data['incident_id'])
        response = self.c.put('/api/v3/incidents/' + incident_id + '/', incident_json_update, format='json')
        self.assertEqual(response.status_code, 200)

        # Next heartbeat call for that device should include the incident ID to fetch the incident.
        response = self.c.post('/api/v3/auth/login/', {'email': self.userPatroller.email, 'password': '1234'},
                               format='json')
        response = self.c.get('/api/v3/devices/' + device_id + '/heartbeat/',
                              {
                                  "resort_id": str(self.resort.resort_id),
                                  "user_id": str(self.userPatroller.user_id)
                              }, format='json')
        # print response
        self.assertEqual(response.data["function"]["getincident"][0], incident_id)

        # Patroller2 registers with a device via API
        response = self.c.post('/api/v3/auth/login/', {'email': self.userPatroller2.email, 'password': '1234'},
                               format='json')
        response = self.c.post('/api/v3/devices/',
                               {"device_push_token": "3a0c0ac71ee49eac8b0444a85f1c16692106c3d3bc50d17f8be",
                                "device_os": "iOS 7.0.2",
                                "device_type": "iPhone 6",
                                "device_connected": 0,
                                "user_id": self.userPatroller2.user_id}, format='json')
        device_id2 = str(response.data['device_id'])
        self.assertEqual(response.status_code, 200)

        # Dispatch changes the assignee away from the device
        incident_json_update["assigned_to"] = str(self.userPatroller2.user_id)
        response = self.c.post('/api/v3/auth/login/', {'email': self.userDispatcher2.email, 'password': '1234'},
                               format='json')
        response = self.c.put('/api/v3/incidents/' + incident_id + '/', incident_json_update, format='json')
        self.assertEqual(response.status_code, 200)

        # Update IncidentAudit dt_created since now() function return the start time of the current transaction,
        # their values do not change during the transaction.
        from apps.incidents.models import Incident
        from apps.incidents.models import IncidentAudit
        incident = Incident.objects.filter(incident_id=incident_id).first()
        incidentAudit = IncidentAudit.objects.filter(incident=incident).order_by("-audit_id").first()
        incidentAudit.dt_created = timezone.now()
        incidentAudit.save()

        # Next heartbeat call should show the incident id in the delete section
        response = self.c.post('/api/v3/auth/login/', {'email': self.userPatroller.email, 'password': '1234'},
                               format='json')

        response = self.c.get('/api/v3/devices/' + device_id + '/heartbeat/',
                              {
                                  "resort_id": str(self.resort.resort_id),
                                  "user_id": str(self.userPatroller.user_id)
                              }, format='json')
        # print response
        self.assertEqual(response.data["function"]["deleteincident"][0], incident_id)


class UserConnectedTestCase(APITestCase):
    def setUp(self):
        self.userPatroller = UserFactory(email='patroller@yahoo.com', name='Mr Patroller',
                                         user_connected=1, is_active=True)
        self.userDispatcher = UserFactory(email='dispatcher@yahoo.com', name='Mr Dispatcher',
                                          user_connected=1, is_active=True)
        self.userManager = UserFactory(email='manager@yahoo.com', name='Mr Manager',
                                       user_connected=1, is_active=True)
        self.application = ApplicationFactory()
        self.incidentTemplate = IncidentTemplateFactory(template_id=1)
        self.domain = DomainFactory(domain_id=1)
        self.domain = DomainFactory(domain='api-dev-au.medic52.com', is_active=True)
        self.domain = DomainFactory(domain='testserver', is_active=True)
        # self.domain = Domains.objects.all()
        # print Domains.objects.get(pk=1), "debug"
        self.resort = ResortFactory(domain_id=self.domain)
        self.userRolePatroller = UserRolesFactory(role_id=1, key='patroller', order=1)
        self.userRoleDispatcher = UserRolesFactory(role_id=2, key='dispatcher', order=2)
        self.userRoleManager = UserRolesFactory(role_id=3, key='manager', order=3)
        self.userResortMapPatroller = UserResortMapFactory(role_id=self.userRolePatroller.role_id,
                                                           user=self.userPatroller, resort=self.resort)
        self.userResortMapDispatcher = UserResortMapFactory(role_id=self.userRoleDispatcher.role_id,
                                                            user=self.userDispatcher, resort=self.resort)
        self.userResortMapManager = UserResortMapFactory(role_id=self.userRoleManager.role_id,
                                                         user=self.userManager, resort=self.resort)
        self.c = APIClient()
        self.token = TokenFactory(user=self.userManager)

    def testNetworkUserList(self):
        # 304 Tests to check solo user on resort not shown in networked user list
        response = self.client.post('/oauth/access_token/', {
            'grant_type': 'client_credentials',
            'client_id': self.application.client_id,
            'client_secret': self.application.client_secret
        })
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {
            'email': self.userManager.email,
            'password': '1234'
        }, format='json')
        # create user using manager account
        response = self.c.post('/api/v3/users/',
                               {
                                   "name": "Mr User 1",
                                   "email": "user1@summit.com",
                                   "password": "SuperSimple2015",
                                   "phone": "0138562894",
                                   "role_id": 1,
                                   "resort_id": str(self.resort.resort_id),
                                   "status": "Active"
                               }, format='json')

        self.assertEqual(response.status_code, 200)

        # When logged in a manager or dispatcher and user_connected = network,
        # user lists should not show user_connected = solo users
        response = self.c.get('/api/v3/users/',
                              {
                                  'offset': 0,
                                  'chunk': 5,
                                  'search': 'M',
                                  'order_by': 'name',
                                  'order_by_direction': 'desc'
                              }, format='json')

        self.assertNotContains(response, '"user_connected":{"value":0,"key":"solo"}')
