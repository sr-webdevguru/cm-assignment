import base64
import json
import os
from datetime import datetime, date, timedelta

from django.conf import settings
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient

from apps.authentication.factory.oauth_factory import ApplicationFactory, TokenFactory
from apps.custom_user.factory.user_factory import UserFactory, UserRolesFactory
from apps.incidents.factory.incident_factory import IncidentStatusFactory, IncidentFactory
from apps.resorts.factory.resort_factory import ResortFactory, IncidentTemplateFactory, UserResortMapFactory
from apps.routing.factory.routing_factory import DomainFactory

INCIDENT_CREATE_JSON = {
    "field_52ca456962ba8": {
        "lat": -27.059125784374054,
        "long": 135,
        "accuracy": 4
    },
    "dt_created": timezone.now().strftime("%Y-%m-%d %H:%M:%S")
}

FULL_INCIDENT_JSON = {
    "field_52dd8c049b005": 32,
    "field_52ca445d62ba6": "pain",
    "field_52ca445d62ba1": [
        "22",
        "102",
        "94",
        "1069",
        "1072",
        "25"
    ],
    "incident_status": {
        "incident_status_id": 1,
        "order": 1,
        "color": "ff0000",
        "key": "call_received"
    },
    "field_52ca4637cc0fe": 34.8,
    "sex": "male",
    "field_52ca456962ba8": {
        "lat": -27.059125784374054,
        "long": 135,
        "accuracy": 4
    },
    "field_52d4798f6d227": [
        {
            "preexisting_injury": "234",
            "body_part": "129",
            "injury_location": "153",
            "injury_type": "157"
        }
    ],
    "field_554f7cbb3d784": "some area",
    "field_52dd8bee9b004": 234,
    "field_52d47a654d1aa": [
        {
            "photo": "25901cf5-b519-41a9-bf73-108c49f08b42",
            "photo_date_taken": "2016-01-13 06:30:29"
        }
    ],
    "field_52d47d6aedbdc": "61b552b1-0427-4bec-ac97-8c1963015665",
    "field_551c8aaa3d786": "some location",
    "field_52ca451a62ba5": "57",
    "email": "xyz@adsd.com",
    "field_539158b37517e": "yes",
    "patient_age": 44,
    "field_52ca445d62bb6": "blood",
    "field_52ca461ccc0fd": 34.5,
    "field_52ca453862ba6": "123",
    "incident_id": "b0592536-cbcd-4312-abc1-403e8036ad60",
    "field_551c8bbb3d785": "some run",
    "name": "Mr. Brown",
    "dob": "1971-06-15",
    "incident_pk": 2267,
    "dateTimeFormat": "YYYY-MM-DD HH:mm:ss",
    "field_52d47b5fdda86": [
        {
            "witness_name": "Mr Alex",
            "witness_phone": "+18956235656",
            "witness_relationship": "friend",
            "witness_date_of_birth": "1981-11-26",
            "witness_type": "79",
            "witness_statement_recording": "2d90f0c2-47ff-42e3-ad75-5db232dda1f6",
            "time_of_witness_statement": "2016-01-19 07:13:23"
        }
    ],
    "address": "oxford county",
    "suburb": "oxford",
    "state": "oxford",
    "postcode": "598563",
    "country": "United Kingdom",
    "phone": "+89565232656",
    "occupation": "Some job",
    "local_accommodation": "Local accommodation",
    "field_52ca3d31ac436": "80",
    "field_5386e4e216667": "496",
    "field_52ca3dc8ac437": "69",
    "field_52ca449b62ba3": "yes",
    "field_52ca44c862ba4": "Mr. experience",
    "field_52d488615b642": "238",
    "field_52ca3dfcac438": "228",
    "field_52ca999b62ba3": "yes",
    "field_52ca988b62ba3": "5",
    "field_52d4888a5b643": 5,
    "field_53f5cabe56646": 3,
    "field_52d488b6573b0": 45,
    "field_52d155b6549d0": 4,
    "field_52ca3e17ac439": "77",
    "field_52d484ebef10b": "63",
    "field_52ca429c62b98": "yes",
    "field_52d483dceb786": [
        "204",
        "206"
    ],
    "field_52ca430462b9a": "yes",
    "field_52dd8a57e95a7": "helmote",
    "field_54b084fb2d255": "yes",
    "field_54b085452d256": "Rental shop",
    "field_52ca431e62b9b": "yes",
    "field_54b083b2ac7a8": "Plastic",
    "field_54b083c3ac7a9": "New model",
    "field_52d48512ef10c": [
        "219",
        "217"
    ],
    "field_52d84412ef10c": "210",
    "field_52ca3ef759d23": 5,
    "field_52ca3f8e59d28": 2,
    "field_52ca3f8d59d27": 13,
    "field_52ca3f8c59d26": 16,
    "field_54b0869fefc8c": "yes",
    "field_52ca42f362b99": "Some rental shop",
    "field_54b087d913f98": "Some ski board",
    "field_54b087ef13f99": "Some boot",
    "field_5530f7ccd3d86": "yes",
    "field_5530f7edd3d87": "Crash",
    "field_52d47f058205b": "yes",
    "field_52d47ef08205a": "Food alergy",
    "field_52ca3fcc59d29": "yes",
    "field_52ca404059d2b": "Scotch",
    "field_52ca3fe959d2a": "yesterday",
    "field_52ca437b62b9c": "yes",
    "field_52ca438e62b9d": "Crosin",
    "field_52ca438f62b9e": "today",
    "field_52ca405959d2c": "yes",
    "field_52ca407959d2d": "some medication",
    "field_52ca407a59d2e": "daily",
    "field_52ca407646d2d": "no other",
    "field_52cfg407646d2d": "today morning",
    "field_52ca43f362ba0": "yes",
    "field_52ca43c462b9f": "yes",
    "field_52d4767cde30d": [
        {
            "gcs_eye": 1,
            "gcs_motor": 2,
            "gcs_verbal": 3,
            "heart_rate": 123,
            "respiration_rate": 200,
            "sp02": 3,
            "blood_pressure": "123",
            "pain_score": 6,
            "skin_colour": "pale",
            "date_added": "2016-01-13 07:18:29"
        }
    ],
    "field_52ca447762ba2": [
        "64",
        "66",
        "67",
        "1115"
    ],
    "field_84d435ysr6dbe2": "yes",
    "field_52d47eer6dbe2": "General patient",
    "field_52d53eer6dbe2": "1083",
    "field_52d435ysr6dbe2": "yes",
    "field_52d435ysr6dbe4": "some person",
    "field_52dabradbe2": "yes",
    "field_52dabradbe3": "mountain life",
    "field_52dabradbe4": "1111",
    "field_52d4800164f2e": [
        {
            "drug_administered": "31",
            "drug_time_administered": "2016-01-13 12:49:31",
            "drug_volume_administered": "527",
            "dose_administered": 143
        }
    ],
    "field_5386e82f7e637": [
        "112",
        "113"
    ],
    "field_52ca45d6cc0fb": [
        "52",
        "104",
        "107"
    ],
    "field_52ca45fbcc0fc": "56",
    "field_54b0805ff5b3f": "1427",
    "field_539158987517d": "yes",
    "field_52ca4c34ef1a1": [
        "48",
        "45"
    ],
    "field_53915a06a08f6": [
        "513",
        "511"
    ],
    "field_89175a06a08f6": "1095",
    "field_52d47d7fedbdd": "yes",
    "field_52d47da6edbde": "some guardian",
    "field_5334b101c8779": "yes",
    "field_53c386190a2dd": "yes",
    "field_52dd8a24e95a6": "yes",
    "field_539158b37814e": "yes",
    "field_539158b37814f": "1395",
    "field_539158b37754f": "none",
    "field_52d48077a16be": "196",
    "field_52d48117a16bf": "Patroller",
    "field_5331c532e16be": "1103",
    "field_5331c532e16df": "1105",
    "field_5331c865e16df": "1109",
    "field_863458b37814e": "yes",
    "field_863458b37814f": "Some signage",
    "field_52d47e4cedbe2": "This case is closed",
    "field_52d47de5edbdf": "4505184a-f89e-4448-928d-ce01f65532ce",
    "notes": [
        {
            "field_52ca448dg94ja4": "2016-01-13 12:51:27",
            "field_52ca448dg94ja3": "One note"
        }
    ]
}


class IncidentsTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user1 = UserFactory(email="userseq1@test.com", user_connected=1)
        self.fake_user = UserFactory(email="fake_user1@test.com", user_connected=1)
        self.solo_user = UserFactory(email='solo_user44@admin.com', name="soloUser1",
                                     user_connected=0)  # user_connected = SOLO
        self.no_resort_user = UserFactory(email='user_net_no_resort212@admin.com', name="UserNoResort",
                                          user_connected=1)  # user_connected = Network
        self.network_user = UserFactory(email='user_net212@admin.com', name="User212",
                                        user_connected=1)  # user_connected = Network
        self.network_user_admin = UserFactory(email='user_net212_admin@admin.com', name="User212", user_connected=1,
                                              is_admin=True)  # user_connected = Network
        self.role1_user = UserFactory(email='user_role1@role1.com', name="User1", user_connected=1)  # user_for role = 1
        self.application = ApplicationFactory()
        self.incidentTemplate = IncidentTemplateFactory(template_id=1)
        self.domain = DomainFactory(domain_id=1, domain='api-dev-us.medic52.com', is_active=True)
        self.domain = DomainFactory(domain_id=2, domain='api-dev-au.medic52.com', is_active=True)
        self.domain = DomainFactory(domain_id=3, domain='testserver12', is_active=True)
        self.resort = ResortFactory(domain_id=self.domain, resort_name='Vanilla Ski aaa111', network_key="tYgK9UjK")
        self.resort1 = ResortFactory(use_sequential_incident_id=1, domain_id=self.domain,
                                     resort_name='Vanilla Ski 784512', network_key="tYpO1UjK")
        self.userRoles = UserRolesFactory(role_id=3, key='manager', order=3)
        self.userRoles1 = UserRolesFactory(role_id=1, key='role1', order=1)
        self.user_resort_map = UserResortMapFactory(user=self.user, resort=self.resort, role_id=3)
        self.user_resort_map = UserResortMapFactory(user=self.solo_user, resort=self.resort, role_id=3)
        self.user_resort_map = UserResortMapFactory(user=self.role1_user, resort=self.resort, role_id=1)
        self.user_resort_map1 = UserResortMapFactory(user=self.user1, resort=self.resort1, role_id=3)
        self.user_resort_map_net = UserResortMapFactory(user=self.network_user, resort=self.resort, role_id=3)
        self.user_resort_map_net_admin = UserResortMapFactory(user=self.network_user_admin, resort=self.resort,
                                                              role_id=3)
        self.incidentStatus = IncidentStatusFactory(incident_status_id=1)
        self.incidentStatus9 = IncidentStatusFactory(order=9, key='status delted or invalid')
        self.incidentStatus8 = IncidentStatusFactory(order=8, key='status order 8')

        resort_users = [{str(self.user.user_id): self.user.name},
                        {str(self.network_user.user_id): self.network_user.name},
                        {str(self.network_user_admin.user_id): self.network_user_admin.name}]
        self.resort.incident_template['DashboardItems']['field_52d47aac9bd13']['RepeatingQuestions']['patroller'][
            'Values'] = resort_users
        self.resort.save()

        from django.db import connection
        with connection.cursor() as c:
            c.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')

        self.c = APIClient()
        self.token = TokenFactory(user=self.user)
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        self.incident1 = IncidentFactory(resort=self.resort, assigned_to=self.user,
                                         incident_status=self.incidentStatus)
        self.c.force_authenticate(user=self.user)
        response = self.c.put('/api/v3/incidents/%s/' % self.incident1.incident_id,
                              FULL_INCIDENT_JSON, format='json')

        self.incident2 = IncidentFactory(resort=self.resort, assigned_to=self.network_user,
                                         incident_status=self.incidentStatus)
        self.c.force_authenticate(user=self.network_user)
        response = self.c.put('/api/v3/incidents/%s/' % self.incident2.incident_id,
                              FULL_INCIDENT_JSON, format='json')

        self.incident3 = IncidentFactory(resort=self.resort, assigned_to=self.network_user,
                                         incident_status=self.incidentStatus)
        self.c.force_authenticate(user=self.network_user)
        response = self.c.put('/api/v3/incidents/%s/' % self.incident3.incident_id,
                              FULL_INCIDENT_JSON, format='json')

        self.incident4 = IncidentFactory(resort=self.resort, assigned_to=self.network_user,
                                         incident_status=self.incidentStatus)
        self.c.force_authenticate(user=self.network_user)
        response = self.c.put('/api/v3/incidents/%s/' % self.incident4.incident_id,
                              FULL_INCIDENT_JSON, format='json')

        self.incident5 = IncidentFactory(resort=self.resort, assigned_to=self.network_user,
                                         incident_status=self.incidentStatus)
        self.c.force_authenticate(user=self.network_user)
        response = self.c.put('/api/v3/incidents/%s/' % self.incident5.incident_id,
                              FULL_INCIDENT_JSON, format='json')

        self.incident6 = IncidentFactory(resort=self.resort, assigned_to=self.network_user_admin,
                                         incident_status=self.incidentStatus)
        self.c.force_authenticate(user=self.network_user_admin)
        response = self.c.put('/api/v3/incidents/%s/' % self.incident6.incident_id,
                              FULL_INCIDENT_JSON, format='json')

        self.incident7 = IncidentFactory(resort=self.resort, assigned_to=self.network_user_admin,
                                         incident_status=self.incidentStatus)
        self.c.force_authenticate(user=self.network_user_admin)
        response = self.c.put('/api/v3/incidents/%s/' % self.incident7.incident_id,
                              FULL_INCIDENT_JSON, format='json')

        self.incident8 = IncidentFactory(resort=self.resort, assigned_to=self.network_user_admin,
                                         incident_status=self.incidentStatus)
        self.c.force_authenticate(user=self.network_user_admin)
        response = self.c.put('/api/v3/incidents/%s/' % self.incident8.incident_id,
                              FULL_INCIDENT_JSON, format='json')
        self.c.force_authenticate(user=None)
        self.fullDataIncidentID = ''

    def testListStatus(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/17/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testListStatus
        """
        from django.db import connection

        with connection.cursor() as c:
            c.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.get('/api/v3/incidents/status/',
                              {}, format='json')
        self.assertEqual(response.status_code, 200)

    def testListOrderASC(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/07/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testListOrderASC
        """
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.get(
            '/api/v3/incidents/?offset=0&chunk=10&resort_id=%s&date_from=%s&order_by_direction=asc' % (
                str(self.resort.resort_id), date.today().strftime("%Y-%m-%d 00:00:01")),
            {}, format='json')
        self.assertEqual(response.status_code, 200)

    def testListAssignedTo(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/07/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testListAssignedTo
        """
        from django.db import connection

        with connection.cursor() as c:
            c.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.get('/api/v3/incidents/?offset=0&chunk=10&resort_id=%s&date_from=%s&assigned_to=%s' % (
            str(self.resort.resort_id), date.today().strftime("%Y-%m-%d 00:00:01"), self.network_user.user_id),
                              {}, format='json')
        self.assertEqual(response.status_code, 200)

    def testListNoDateFrom(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/07/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testListNoDateFrom
        """
        from django.db import connection

        with connection.cursor() as c:
            c.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.get('/api/v3/incidents/?offset=0&chunk=10&resort_id=%s' % (str(self.resort.resort_id)),
                              {}, format='json')
        self.assertEqual(response.status_code, 200)

    def testListWithDateTo(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/07/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testListWithDateTo
        """
        from django.db import connection

        with connection.cursor() as c:
            c.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.get('/api/v3/incidents/?offset=0&chunk=10&resort_id=%s&date_to=%s' % (
            str(self.resort.resort_id), date.today().strftime("%Y-%m-%d 11:59:59")),
                              {}, format='json')
        self.assertEqual(response.status_code, 200)

    def testListInvalidResortUUID(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/12/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testListInvalidResortUUID
        """
        from django.db import connection

        with connection.cursor() as c:
            c.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.get('/api/v3/incidents/?offset=0&chunk=10&resort_id=%s' % ("hahaha489jk"),
                              {}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['detail'], "not_a_valid_uuid")

    def testListResortNotExist(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/12/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testListResortNotExist
        """
        from django.db import connection

        with connection.cursor() as c:
            c.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.get('/api/v3/incidents/?offset=0&chunk=10&resort_id=%s' % (self.network_user.user_id),
                              {}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['detail'], "resort_does_not_exists")

    def testListAssignedToInvalid(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/15/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testListAssignedToInvalid
        """
        from django.db import connection

        with connection.cursor() as c:
            c.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.get('/api/v3/incidents/?offset=0&chunk=10&assigned_to=%s' % (self.incident.incident_id),
                              {}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['detail'], "assigned_to_user_does_not_exists")

    def testListNoResortIdNotAdmin(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/07/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testListNoResortIdNotAdmin
        """
        from django.db import connection

        with connection.cursor() as c:
            c.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.get('/api/v3/incidents/?offset=0&chunk=10&date_from=%s&order_by_direction=asc' % (
            date.today().strftime("%Y-%m-%d 00:00:01")),
                              {}, format='json')
        self.assertEqual(response.status_code, 200)

    def testListNoResortIdAdmin(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/07/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testListNoResortIdAdmin
        """
        from django.db import connection

        with connection.cursor() as c:
            c.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user_admin.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.get('/api/v3/incidents/?offset=0&chunk=10&date_from=%s&order_by_direction=asc' % (
            timezone.now().strftime("%Y-%m-%d 00:00:01")),
                              {}, format='json')
        self.assertEqual(response.status_code, 200)

    def testListValidResortIdAdmin(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/07/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testListValidResortIdAdmin
        """
        from django.db import connection

        with connection.cursor() as c:
            c.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user_admin.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.get('/api/v3/incidents/?offset=0&chunk=10&resort_id=%s&date_to=%s' % (
            str(self.resort.resort_id), date.today().strftime("%Y-%m-%d 00:00:01")),
                              {}, format='json')
        self.assertEqual(response.status_code, 200)

    def testUpdateIncidentSOLO(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/07/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testUpdateIncidentSOLO
        """
        from django.db import connection

        with connection.cursor() as c:
            c.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.post('/api/v3/incidents/',
                               INCIDENT_CREATE_JSON, format='json')

        self.assertEqual(response.status_code, 200)
        incident_id = response.data['incident_id']

        # Switch to user with role1 then try to update incident
        response = self.c.post('/api/v3/auth/login/', {'email': self.solo_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.put('/api/v3/incidents/%s/' % incident_id,
                              FULL_INCIDENT_JSON, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.content)['detail'], "You do not have permission to edit this incident")

    def testGetIncidentInjuries(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/23/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testGetIncidentInjuries
        """
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.post('/api/v3/incidents/',
                               FULL_INCIDENT_JSON, format='json')

        self.assertEqual(response.status_code, 200)
        incident_id = response.data['incident_id']
        response = self.c.get('/api/v3/incidents/?offset=0&chunk=10&resort_id=%s&date_from=%s' % (
            str(self.resort.resort_id), date.today().strftime("%Y-%m-%d 00:00:01")),
                              {}, format='json')
        self.assertEqual(response.status_code, 200)

    def testUpdateIncidentRole1(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/07/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testUpdateIncidentRole1
        """
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.post('/api/v3/incidents/',
                               INCIDENT_CREATE_JSON, format='json')

        self.assertEqual(response.status_code, 200)
        incident_id = response.data['incident_id']

        # Switch to user with role1 then try to update incident
        response = self.c.post('/api/v3/auth/login/', {'email': self.role1_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.put('/api/v3/incidents/%s/' % incident_id,
                              FULL_INCIDENT_JSON, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.content)['detail'], "You do not have permission to edit this incident")

    def testUpdateIncidentStatusOrder9(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/07/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testUpdateIncidentStatusOrder9
        """
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.post('/api/v3/incidents/',
                               INCIDENT_CREATE_JSON, format='json')

        self.assertEqual(response.status_code, 200)
        incident_id = response.data['incident_id']

        response = self.c.post('/api/v3/incidents/%s/status/' % incident_id,
                               {"status_type_id": self.incidentStatus9.incident_status_id,
                                "status_date": date.today().strftime("%Y-%m-%d %H:%M:%S"),
                                "updated_by": self.network_user.user_id}, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.put('/api/v3/incidents/%s/' % incident_id,
                              FULL_INCIDENT_JSON, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['detail'], "incident_does_not_exist")

    def testUpdateIncidentInvalidAssignedTo(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/13/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testUpdateIncidentInvalidAssignedTo
        """
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.post('/api/v3/incidents/',
                               INCIDENT_CREATE_JSON, format='json')

        self.assertEqual(response.status_code, 200)
        incident_id = response.data['incident_id']

        update_incident_json = FULL_INCIDENT_JSON
        update_incident_json.update({'assigned_to': incident_id})

        response = self.c.put('/api/v3/incidents/%s/' % incident_id,
                              update_incident_json, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['detail'], "assigned_user_does_not_exist")

    def testUpdateIncidentDifferentAssignedTo(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/13/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testUpdateIncidentDifferentAssignedTo
        """
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.role1_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.post('/api/v3/incidents/',
                               INCIDENT_CREATE_JSON, format='json')

        self.assertEqual(response.status_code, 200)
        incident_id = response.data['incident_id']

        update_incident_json = FULL_INCIDENT_JSON
        update_incident_json.update({
            "assigned_to": self.network_user_admin.user_id
        })

        response = self.c.put('/api/v3/incidents/%s/' % incident_id,
                              update_incident_json, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.content)['detail'], "You do not have permission to assign this incident")

    def testUpdateIncidentFutureDTCreated(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/13/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testUpdateIncidentFutureDTCreated
        """
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.post('/api/v3/incidents/',
                               INCIDENT_CREATE_JSON, format='json')

        self.assertEqual(response.status_code, 200)
        incident_id = response.data['incident_id']

        update_incident_json = FULL_INCIDENT_JSON
        update_incident_json.update({
            "dt_created": (date.today() + timedelta(days=1)).strftime("%Y-%m-%d 00:00:01")
        })

        response = self.c.put('/api/v3/incidents/%s/' % incident_id,
                              update_incident_json, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['detail'], "dt_created_can_not_be_a_future_date")

    def testRetrieveIncidentStatusOrder9(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/12/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testRetrieveIncidentStatusOrder9
        """
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.post('/api/v3/incidents/',
                               INCIDENT_CREATE_JSON, format='json')

        self.assertEqual(response.status_code, 200)
        incident_id = response.data['incident_id']

        response = self.c.post('/api/v3/incidents/%s/status/' % incident_id,
                               {"status_type_id": self.incidentStatus9.incident_status_id,
                                "status_date": date.today().strftime("%Y-%m-%d %H:%M:%S"),
                                "updated_by": self.network_user.user_id}, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.get('/api/v3/incidents/%s/' % incident_id,
                              {}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['detail'], "incident_does_not_exist")

    def testRetrieveIncidentInvalidPermissions(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/12/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testRetrieveIncidentInvalidPermissions
        """
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.post('/api/v3/incidents/',
                               INCIDENT_CREATE_JSON, format='json')

        self.assertEqual(response.status_code, 200)
        incident_id = response.data['incident_id']

        response = self.c.post('/api/v3/auth/login/', {'email': self.solo_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.get('/api/v3/incidents/%s/' % incident_id,
                              {}, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.content)['detail'], "you_do_not_have_permission_to_retrieve_the_incident")

    def testCreateInvalidData(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/07/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         - #TODO PENDING fix resort = None when getting resort for user. this will generate an exception in the incident save.
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testCreateInvalidData
        """
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.no_resort_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        incident_json = {
            "name": "Gary Barlow",
            "email": "garry@barrlow.com",
            "phone": "+50672514236",
            "dob": "two thousand fiveteen, wrong date",
            "sex": "wrong sex",
            "address": "5th Avenue, San Diego",
            "suburb": "Los Ranchos",
            "state": "California",
            "country": "United States",
            "postcode": "12152",
            "field_52d47a654d1cc": "a",
            "field_52d47a654d1dd": "garry@barrlow.com",
            "field_52d47a654d1ee": "two thousand fiveteen, wrong date",
            "field_52d47a654d1ff": "wrong sex",
            "field_52d47a654d1bb": "Gary Barlow"
        }

        response = self.c.post('/api/v3/incidents/',
                               incident_json, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['detail'], "invalid_incident_information_provided")

    def testCreateWithSequentialId1(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/07/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         - PENDING fix.
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testCreateWithSequentialId1
        """
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user1.email, 'password': '1234'}, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.post('/api/v3/incidents/',
                               INCIDENT_CREATE_JSON, format='json')

        self.assertEqual(response.status_code, 200)

    def testRetrieveWithSequentialId1(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/12/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         - PENDING fix from create incident api with sequential id = 1
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testRetrieveWithSequentialId1
        """
        from django.db import connection

        with connection.cursor() as c:
            c.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user1.email, 'password': '1234'}, format='json')
        self.assertEqual(response.status_code, 200)

        incident_json = {
            "name": "Gary Barlow",
            "email": "garry@barrlow.com",
            "phone": "+50672514236",
            "dob": "1978-07-15",
            "sex": "male",
            "address": "5th Avenue, San Diego",
            "suburb": "Los Ranchos",
            "state": "California",
            "country": "United States",
            "postcode": "12152"
        }

        response = self.c.post('/api/v3/incidents/',
                               incident_json, format='json')

        self.assertEqual(response.status_code, 200)
        incident_id = response.data['incident_id']

        response = self.c.get('/api/v3/incidents/%s/' % incident_id,
                              {}, format='json')
        self.assertEqual(response.status_code, 200)

    def testPatientDataInvalidPK(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/17/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testPatientDataInvalidPK
        """
        from django.db import connection

        with connection.cursor() as c:
            c.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        incident_json = {
            "name": "Gary Barlow",
            "email": "garry@barrlow.com",
            "phone": "+50672514236",
            "dob": "1978-07-15",
            "sex": "male",
            "address": "5th Avenue, San Diego",
            "suburb": "Los Ranchos",
            "state": "California",
            "country": "United States",
            "postcode": "12152"
        }

        response = self.c.post('/api/v3/incidents/',
                               incident_json, format='json')

        self.assertEqual(response.status_code, 200)
        incident_id = response.data['incident_id']

        response = self.c.post('/api/v3/incidents/%s/status/' % incident_id,
                               {"status_type_id": self.incidentStatus9.incident_status_id,
                                "status_date": date.today().strftime("%Y-%m-%d %H:%M:%S"),
                                "updated_by": self.network_user.user_id}, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.get('/api/v3/incidents/%s/print/' % incident_id,
                              {}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['detail'], "incident does not exists")

    def testPrintInvalidPK(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/17/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testPrintInvalidPK
        """
        from django.db import connection

        with connection.cursor() as c:
            c.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        incident_json = {
            "name": "Gary Barlow",
            "email": "garry@barrlow.com",
            "phone": "+50672514236",
            "dob": "1978-07-15",
            "sex": "male",
            "address": "5th Avenue, San Diego",
            "suburb": "Los Ranchos",
            "state": "California",
            "country": "United States",
            "postcode": "12152"
        }

        response = self.c.post('/api/v3/incidents/',
                               incident_json, format='json')

        self.assertEqual(response.status_code, 200)
        incident_id = response.data['incident_id']

        response = self.c.post('/api/v3/incidents/%s/status/' % incident_id,
                               {"status_type_id": self.incidentStatus9.incident_status_id,
                                "status_date": date.today().strftime("%Y-%m-%d %H:%M:%S"),
                                "updated_by": self.network_user.user_id}, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.get('/api/v3/incidents/%s/print/' % incident_id,
                              {}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['detail'], "incident does not exists")

    def testStatusIncidentOrder9(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/17/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         - PENDING fix for unhandled exception.
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testStatusIncidentOrder9
        """
        from django.db import connection

        with connection.cursor() as c:
            c.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        incident_json = {
            "name": "Gary Barlow",
            "email": "garry@barrlow.com",
            "phone": "+50672514236",
            "dob": "1978-07-15",
            "sex": "male",
            "address": "5th Avenue, San Diego",
            "suburb": "Los Ranchos",
            "state": "California",
            "country": "United States",
            "postcode": "12152"
        }

        response = self.c.post('/api/v3/incidents/',
                               incident_json, format='json')

        self.assertEqual(response.status_code, 200)
        incident_id = response.data['incident_id']

        response = self.c.post('/api/v3/incidents/%s/status/' % incident_id,
                               {"status_type_id": self.incidentStatus9.incident_status_id,
                                "status_date": date.today().strftime("%Y-%m-%d %H:%M:%S"),
                                "updated_by": self.network_user.user_id}, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.post('/api/v3/incidents/%s/status/' % incident_id,
                               {"status_type_id": self.incidentStatus9.incident_status_id,
                                "status_date": date.today().strftime("%Y-%m-%d %H:%M:%S"),
                                "updated_by": self.network_user.user_id}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['detail'], "incident does not exists")

    def testStatusGetIncidentOrder9(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/17/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         - PENDING fix for unhandled exception.
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testStatusGetIncidentOrder9
        """
        from django.db import connection

        with connection.cursor() as c:
            c.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        incident_json = {
            "name": "Gary Barlow",
            "email": "garry@barrlow.com",
            "phone": "+50672514236",
            "dob": "1978-07-15",
            "sex": "male",
            "address": "5th Avenue, San Diego",
            "suburb": "Los Ranchos",
            "state": "California",
            "country": "United States",
            "postcode": "12152"
        }

        response = self.c.post('/api/v3/incidents/',
                               incident_json, format='json')

        self.assertEqual(response.status_code, 200)
        incident_id = response.data['incident_id']

        response = self.c.post('/api/v3/incidents/%s/status/' % incident_id,
                               {"status_type_id": self.incidentStatus9.incident_status_id,
                                "status_date": date.today().strftime("%Y-%m-%d %H:%M:%S"),
                                "updated_by": self.network_user.user_id}, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.get('/api/v3/incidents/%s/status/' % incident_id,
                              {}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['detail'], "incident_does_not_exists")

    def testStatusGetInvalidUUID(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/19/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testStatusGetInvalidUUID
        """
        from django.db import connection

        with connection.cursor() as c:
            c.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.get('/api/v3/incidents/%s/status/' % "asdasd8464a6",
                              {}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['detail'], "not_a_valid_uuid")

    def testStatusGetIncidentNotExist(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/19/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testStatusGetIncidentNotExist
        """
        from django.db import connection

        with connection.cursor() as c:
            c.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.get('/api/v3/incidents/%s/status/' % self.network_user.user_id,
                              {}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['detail'], "incident_does_not_exists")

    def testStatusIncidentOrder8Role1(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/19/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         - PENDING fix for unhandled exception.
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testStatusIncidentOrder8Role1
        """
        from django.db import connection

        with connection.cursor() as c:
            c.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.role1_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        incident_json = {
            "name": "Gary Barlow",
            "email": "garry@barrlow.com",
            "phone": "+50672514236",
            "dob": "1978-07-15",
            "sex": "male",
            "address": "5th Avenue, San Diego",
            "suburb": "Los Ranchos",
            "state": "California",
            "country": "United States",
            "postcode": "12152"
        }

        response = self.c.post('/api/v3/incidents/',
                               incident_json, format='json')

        self.assertEqual(response.status_code, 200)
        incident_id = response.data['incident_id']

        response = self.c.post('/api/v3/incidents/%s/status/' % incident_id,
                               {"status_type_id": self.incidentStatus8.incident_status_id,
                                "status_date": date.today().strftime("%Y-%m-%d %H:%M:%S"),
                                "updated_by": self.role1_user.user_id}, format='json')
        self.assertEqual(response.status_code, 200)
        response = self.c.post('/api/v3/incidents/%s/status/' % incident_id,
                               {"status_type_id": self.incidentStatus8.incident_status_id,
                                "status_date": date.today().strftime("%Y-%m-%d %H:%M:%S"),
                                "updated_by": self.role1_user.user_id}, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.content)['detail'], "You do not have permission to open this incident")

    def testStatusNotFound(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/19/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testStatusNotFound
        """
        from django.db import connection

        with connection.cursor() as c:
            c.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        incident_json = {
            "name": "Gary Barlow",
            "email": "garry@barrlow.com",
            "phone": "+50672514236",
            "dob": "1978-07-15",
            "sex": "male",
            "address": "5th Avenue, San Diego",
            "suburb": "Los Ranchos",
            "state": "California",
            "country": "United States",
            "postcode": "12152"
        }

        response = self.c.post('/api/v3/incidents/',
                               incident_json, format='json')

        self.assertEqual(response.status_code, 200)
        incident_id = response.data['incident_id']

        response = self.c.post('/api/v3/incidents/%s/status/' % incident_id,
                               {"status_type_id": -1,
                                "status_date": date.today().strftime("%Y-%m-%d %H:%M:%S"),
                                "updated_by": self.network_user.user_id}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['detail'], "incident_status_not_found")

    def testStatusUpdatedByNotFound(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/19/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testStatusUpdatedByNotFound
        """
        from django.db import connection

        with connection.cursor() as c:
            c.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        incident_json = {
            "name": "Gary Barlow",
            "email": "garry@barrlow.com",
            "phone": "+50672514236",
            "dob": "1978-07-15",
            "sex": "male",
            "address": "5th Avenue, San Diego",
            "suburb": "Los Ranchos",
            "state": "California",
            "country": "United States",
            "postcode": "12152"
        }

        response = self.c.post('/api/v3/incidents/',
                               incident_json, format='json')

        self.assertEqual(response.status_code, 200)
        incident_id = response.data['incident_id']

        response = self.c.post('/api/v3/incidents/%s/status/' % incident_id,
                               {"status_type_id": self.incidentStatus.incident_status_id,
                                "status_date": date.today().strftime("%Y-%m-%d %H:%M:%S"),
                                "updated_by": incident_id}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['detail'], "updated_by_user_not_found")

    def testStatusInvalidIncidentUUID(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/19/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testStatusInvalidIncidentUUID
        """
        from django.db import connection

        with connection.cursor() as c:
            c.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)
        response = self.c.post('/api/v3/incidents/%s/status/' % "asdoiasiduqibdiq923193192",
                               {"status_type_id": self.incidentStatus9.incident_status_id,
                                "status_date": date.today().strftime("%Y-%m-%d %H:%M:%S"),
                                "updated_by": self.network_user.user_id}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['detail'], "not_a_valid_uuid")

    def testStatusIncidentNotExist(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/19/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testStatusIncidentNotExist
        """
        from django.db import connection

        with connection.cursor() as c:
            c.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)
        response = self.c.post('/api/v3/incidents/%s/status/' % self.network_user.user_id,
                               {"status_type_id": self.incidentStatus.incident_status_id,
                                "status_date": date.today().strftime("%Y-%m-%d %H:%M:%S"),
                                "updated_by": self.network_user.user_id}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['detail'], "incident does not exists")

    def testPatientIncidentStatus9(self):
        """
        Purpose - Code Coverage
        Ticket no - #332
        Date created - 08/19/2015
        Date updated -
        Updates made:
         - Code Coverage
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testPatientIncidentStatus9
        """
        from django.db import connection

        with connection.cursor() as c:
            c.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        incident_json = {
            "name": "Gary Barlow",
            "email": "garry@barrlow.com",
            "phone": "+50672514236",
            "dob": "1978-07-15",
            "sex": "male",
            "address": "5th Avenue, San Diego",
            "suburb": "Los Ranchos",
            "state": "California",
            "country": "United States",
            "postcode": "12152"
        }

        response = self.c.post('/api/v3/incidents/',
                               incident_json, format='json')

        self.assertEqual(response.status_code, 200)
        incident_id = response.data['incident_id']

        response = self.c.post('/api/v3/incidents/%s/status/' % incident_id,
                               {"status_type_id": self.incidentStatus9.incident_status_id,
                                "status_date": date.today().strftime("%Y-%m-%d %H:%M:%S"),
                                "updated_by": self.network_user.user_id}, format='json')
        self.assertEqual(response.status_code, 200)
        response = self.c.get('/api/v3/incidents/' + str(incident_id) + '/patient/', format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['detail'], "incident_does_not_exists")

    def testEncryptedPatientData(self):
        """
        Purpose - Test verify encryption of patients data
        Ticket no - #247
        Date created - 07/20/2015
        Date updated - 07/21/2015
        Updates made:
         - Test verify encryption of patients data
        Additional comment:
         - Test verify encryption of patients data
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testEncryptedPatientData
        """
        from django.db import connection

        with connection.cursor() as c:
            c.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')
        self.assertEqual(response.status_code, 200)

        incident_json = {
            "name": "Gary Barlow",
            "email": "garry@barrlow.com",
            "phone": "+50672514236",
            "dob": "1978-07-15",
            "sex": "male",
            "address": "5th Avenue, San Diego",
            "suburb": "Los Ranchos",
            "state": "California",
            "country": "United States",
            "postcode": "12152"
        }

        response = self.c.post('/api/v3/incidents/',
                               incident_json, format='json')

        self.assertEqual(response.status_code, 200)
        self.fullDataIncidentID = response.data['incident_id']

        response = self.c.get('/api/v3/incidents/' + str(self.fullDataIncidentID) + '/', format='json')
        self.assertEqual(response.status_code, 200)

        incident_pk = json.loads(response.content)['incident_pk']

        with connection.cursor() as c:
            c.execute(
                "SELECT incident_data  FROM incidents_incident where incident_id = '%s'" % str(self.fullDataIncidentID))

            incident_data_raw = c.fetchone()

        with connection.cursor() as c:
            c.execute(
                "SELECT name, address, suburb, state, postcode, phone, email, dob  FROM incidents_patients where incident_id = '%s'" % str(
                    incident_pk))

            incident_patient_raw = c.fetchone()

        response = self.c.get('/api/v3/incidents/' + str(self.fullDataIncidentID) + '/patient/', format='json')
        self.assertEqual(response.status_code, 200)
        non_encrypted_data = json.loads(response.content)

        self.assertNotEqual(non_encrypted_data["name"], incident_patient_raw[0], "NOT encrypted")
        self.assertNotEqual(non_encrypted_data["address"], incident_patient_raw[1], "NOT encrypted")
        self.assertNotEqual(non_encrypted_data["suburb"], incident_patient_raw[2], "NOT encrypted")
        self.assertNotEqual(non_encrypted_data["state"], incident_patient_raw[3], "NOT encrypted")
        self.assertNotEqual(non_encrypted_data["postcode"], incident_patient_raw[4], "NOT encrypted")
        self.assertNotEqual(non_encrypted_data["phone"], incident_patient_raw[5], "NOT encrypted")
        self.assertNotEqual(non_encrypted_data["email"], incident_patient_raw[6], "NOT encrypted")
        self.assertNotEqual(non_encrypted_data["dob"], incident_patient_raw[7], "NOT encrypted")

        # UPDATE the Incident to re-validate same data is applied/saved
        update_incident_json = {
            "name": "Gary Barlow",
            "email": "garry@barrlow.com",
            "phone": "+50672514236",
            "dob": "1978-07-15",
            "sex": "male",
            "address": "5th Avenue, San Diego",
            "suburb": "Los Ranchos",
            "state": "California",
            "country": "United States",
            "postcode": "12152"
        }

        response = self.c.put('/api/v3/incidents/%s/' % str(self.fullDataIncidentID),
                              update_incident_json, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.get('/api/v3/incidents/' + str(self.fullDataIncidentID) + '/patient/', format='json')
        self.assertEqual(response.status_code, 200)
        non_encrypted_updated_data = json.loads(response.content)

        self.assertEqual(non_encrypted_data["name"], non_encrypted_updated_data["name"],
                         "Updated with same value but returned different value.")
        self.assertEqual(non_encrypted_data["address"], non_encrypted_updated_data["address"],
                         "Updated with same value but returned different value.")
        self.assertEqual(non_encrypted_data["suburb"], non_encrypted_updated_data["suburb"],
                         "Updated with same value but returned different value.")
        self.assertEqual(non_encrypted_data["state"], non_encrypted_updated_data["state"],
                         "Updated with same value but returned different value.")
        self.assertEqual(non_encrypted_data["postcode"], non_encrypted_updated_data["postcode"],
                         "Updated with same value but returned different value.")
        self.assertEqual(non_encrypted_data["phone"], non_encrypted_updated_data["phone"],
                         "Updated with same value but returned different value.")
        self.assertEqual(non_encrypted_data["email"], non_encrypted_updated_data["email"],
                         "Updated with same value but returned different value.")
        self.assertEqual(non_encrypted_data["dob"], non_encrypted_updated_data["dob"],
                         "Updated with same value but returned different value.")

        # UPDATE the Incident to validate different data is applied/saved
        update_incident_json = {
            "name": "Gary1 Barlow1",
            "email": "garry1@barrlow1.com",
            "phone": "+78572514236",
            "dob": "1981-07-15",
            "sex": "female",
            "address": "5th Avenue1, San Diego",
            "suburb": "Los Ranchos1",
            "state": "California1",
            "country": "Australia",
            "postcode": "12153"
        }

        response = self.c.put('/api/v3/incidents/%s/' % str(self.fullDataIncidentID),
                              update_incident_json, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.get('/api/v3/incidents/' + str(self.fullDataIncidentID) + '/patient/', format='json')
        self.assertEqual(response.status_code, 200)
        non_encrypted_updated_data1 = json.loads(response.content)

        self.assertNotEqual(non_encrypted_data["name"], non_encrypted_updated_data1["name"],
                            "Updated with DIFFERENT value but returned SAME value.")
        self.assertNotEqual(non_encrypted_data["address"], non_encrypted_updated_data1["address"],
                            "Updated with DIFFERENT value but returned SAME value.")
        self.assertNotEqual(non_encrypted_data["suburb"], non_encrypted_updated_data1["suburb"],
                            "Updated with DIFFERENT value but returned SAME value.")
        self.assertNotEqual(non_encrypted_data["state"], non_encrypted_updated_data1["state"],
                            "Updated with DIFFERENT value but returned SAME value.")
        self.assertNotEqual(non_encrypted_data["postcode"], non_encrypted_updated_data1["postcode"],
                            "Updated with DIFFERENT value but returned SAME value.")
        self.assertNotEqual(non_encrypted_data["phone"], non_encrypted_updated_data1["phone"],
                            "Updated with DIFFERENT value but returned SAME value.")
        self.assertNotEqual(non_encrypted_data["email"], non_encrypted_updated_data1["email"],
                            "Updated with DIFFERENT value but returned SAME value.")
        self.assertNotEqual(non_encrypted_data["dob"], non_encrypted_updated_data1["dob"],
                            "Updated with same value but returned SAME value.")

    def testMobileMedia(self):
        # print self.domain.pk
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        # print response.content
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')
        response = self.c.post('/api/v3/incidents/' + str(self.incident.incident_id) + '/media/',
                               {
                                   "mimeType": "image/png",
                                   "media": "iVBORw0KGgoAAAANSUhEUgAAAB8AAAAeCAYAAADU8sWcAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAABQ5JREFUeNqclw1MlVUYx18uN0hGkYWJYFPS3LK6ViS1JX5VmqFpDtFhhrY+wcpMsWzOj+mKghppSiWGmSzXyrIsy0qKyo8MKyKaWRRaimFL0jI/0P/Dfq87u/G1zvbbC+89933O+3/+z3POjVif0NXrwDhbDBXXi1TRV3QSJ/m8QXwttor3uB5v76ER7QQ/X+SI28UF3Nst9vHwf8WZojv4Y4coFGvaWkSwjcA3inwREkdEgXhZ1IrDzDkhIkU0Cx0hpoj+zL1b3Icq/xmBFu5FEuhdAtuYJ2bykEaCnnAWEC8WiF9JywBRIdLEpyK7I8Ht/2LxEA9ayn2TvVsryt2LzJP420admCueEmeIUnFPe8FN5jvELjFa5Ioy0Uc8GjY3FXMtIcDjYqF4SdSIj0Q/8TBpWiYyWwt+i5gh/hC3ii+5PweD2UJG8h0LUk4FfCVuYN4TIkNcJYaJ61DHf+tCx7ing8cjkY0HKBV//CRmOV/ejgp/iywxGIlzeIaVYIrYiEeuxHzPURGPhQe3nPYUq5kYPj4XvyC/Sfk8Eh5E0j0srIZnFGLansz1WKB5YaIY7gePoSQ85+1P9wFKxxzbAxVGMD9WrBdjUWs/ss/he3b/ZpSyUS8W8fckP7jJdqHYJCqdwJci3QrRRTyDQha8RPwg1lERUfjAPHCUUhvNIsucZ77FIs073QK41sZrXGOp2a0Y5kNxLeViQZPFKOYv4zsVGHITJXoehrTGs5YF29grvhBxFteCX8EHn2COCqSz5jENJ28R08n7GHp8L1xtnfBn8YpTSn/R9eJoUCHn7d/mepkF7y124l4zy+XIk0nz8DePRlycIL4R31E2lZSXff49pTpIPEibNbV+F2/ihVqel2DBE8mZ1fJscReBLcjHeMIj5+bszUjaCUdHo8wCpH9VPOsEnC8eYZM56SiQGGRn8nv6BrFS3Elj2E4HS2U3K8CcDahTy65VJS7iaia8SQwRUx2VsinFfcRrCpKfOEyynFxn0WKnUma2oEtEtRhn+RLvsKAJlNpwFlpCddhbH0ChEkp6BwZu3poD1G4XHJ1Kb97FBLs+TestdfpBVzaaeKriajGZN16KURP5/gz8MIW0+gavD2B9j8k72TqTqcX3xYtI/Rv57oWMDZRRkHQNZVebjk9W4ZsXqKJS55xg49sgrdPGQDb+daix32mJh+lWfdj5JtBk8vBBDbLa7laEIjWkY6Njsh4sxCpicwDnWrB0TizJyBhiI6hD7jrqeRi1Xs3ONxNjZlIRMTj8mrDAHs2pM4odCFDfRXw4GwNuoxefI86lJ08jWCnG+gAVFmOkNJ5xEKkbwwInObtjcwoiJ8ZaN21uDhn05B8pD383G8+9Mh6cT7nEcFBIp23eT20PItevhwUvoPxW+S8bcFabx99FSGbjT/KWRo5n0fuHcNy6mK6YwtvMJYVZ+MIfuTSvvajruW/uv30UOU3nrfdQAdHMSSFYfxaTjRKH+PwQ6crgBVaykGK622T3oOIG9zBfEtKNw2RVNIZjbB5niSfZk6taOHhUY9qB7Iq3UQU5SN7qAbIJZ+fzK2U1W2cIR49n48kjVa2Nz7jarvcPKSjuyLm9CSONoXePpRFtQP4G2nEk86Nozf0421U6R6dyGs6a//NzKQ6j5NIg/MXtxjxHUCiJg0MEc7aRmjfa+rkU0cEfijEcKgYgZYiFeRipnvyXcyjZErZ9tjhOCTAAzLFqzz+kWboAAAAASUVORK5CYII="
                               }, format='json')
        # print response
        self.assertEqual(response.status_code, 200)

        media_url = response.data['media_url']

        response = self.c.get(media_url, {}, format='json')
        # print response.data
        self.assertEqual(response.status_code, 200)

        self.d = APIClient()
        response = self.d.get(media_url, {}, format='json')
        # print response
        response_json = json.loads(response.content)
        self.assertEqual(response_json['detail'], 'authentication_credentials_were_not_provided')

    def testMediaInvalidPK(self):
        """
        Purpose - Test POST media with invalid incident pk
        Ticket no - #332
        Date created - 08/14/2015
        Date updated - 08/14/2015
        Updates made:
         -
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testMediaInvalidPK
        """
        # print self.domain.pk
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        # print response.content
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')
        response = self.c.post('/api/v3/incidents/' + str(self.user.user_id) + '/media/',
                               {
                                   "mimeType": "image/png",
                                   "media": "iVBORw0KGgoAAAANSUhEUgAAAB8AAAAeCAYAAADU8sWcAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAABQ5JREFUeNqclw1MlVUYx18uN0hGkYWJYFPS3LK6ViS1JX5VmqFpDtFhhrY+wcpMsWzOj+mKghppSiWGmSzXyrIsy0qKyo8MKyKaWRRaimFL0jI/0P/Dfq87u/G1zvbbC+89933O+3/+z3POjVif0NXrwDhbDBXXi1TRV3QSJ/m8QXwttor3uB5v76ER7QQ/X+SI28UF3Nst9vHwf8WZojv4Y4coFGvaWkSwjcA3inwREkdEgXhZ1IrDzDkhIkU0Cx0hpoj+zL1b3Icq/xmBFu5FEuhdAtuYJ2bykEaCnnAWEC8WiF9JywBRIdLEpyK7I8Ht/2LxEA9ayn2TvVsryt2LzJP420admCueEmeIUnFPe8FN5jvELjFa5Ioy0Uc8GjY3FXMtIcDjYqF4SdSIj0Q/8TBpWiYyWwt+i5gh/hC3ii+5PweD2UJG8h0LUk4FfCVuYN4TIkNcJYaJ61DHf+tCx7ing8cjkY0HKBV//CRmOV/ejgp/iywxGIlzeIaVYIrYiEeuxHzPURGPhQe3nPYUq5kYPj4XvyC/Sfk8Eh5E0j0srIZnFGLansz1WKB5YaIY7gePoSQ85+1P9wFKxxzbAxVGMD9WrBdjUWs/ss/he3b/ZpSyUS8W8fckP7jJdqHYJCqdwJci3QrRRTyDQha8RPwg1lERUfjAPHCUUhvNIsucZ77FIs073QK41sZrXGOp2a0Y5kNxLeViQZPFKOYv4zsVGHITJXoehrTGs5YF29grvhBxFteCX8EHn2COCqSz5jENJ28R08n7GHp8L1xtnfBn8YpTSn/R9eJoUCHn7d/mepkF7y124l4zy+XIk0nz8DePRlycIL4R31E2lZSXff49pTpIPEibNbV+F2/ihVqel2DBE8mZ1fJscReBLcjHeMIj5+bszUjaCUdHo8wCpH9VPOsEnC8eYZM56SiQGGRn8nv6BrFS3Elj2E4HS2U3K8CcDahTy65VJS7iaia8SQwRUx2VsinFfcRrCpKfOEyynFxn0WKnUma2oEtEtRhn+RLvsKAJlNpwFlpCddhbH0ChEkp6BwZu3poD1G4XHJ1Kb97FBLs+TestdfpBVzaaeKriajGZN16KURP5/gz8MIW0+gavD2B9j8k72TqTqcX3xYtI/Rv57oWMDZRRkHQNZVebjk9W4ZsXqKJS55xg49sgrdPGQDb+daix32mJh+lWfdj5JtBk8vBBDbLa7laEIjWkY6Njsh4sxCpicwDnWrB0TizJyBhiI6hD7jrqeRi1Xs3ONxNjZlIRMTj8mrDAHs2pM4odCFDfRXw4GwNuoxefI86lJ08jWCnG+gAVFmOkNJ5xEKkbwwInObtjcwoiJ8ZaN21uDhn05B8pD383G8+9Mh6cT7nEcFBIp23eT20PItevhwUvoPxW+S8bcFabx99FSGbjT/KWRo5n0fuHcNy6mK6YwtvMJYVZ+MIfuTSvvajruW/uv30UOU3nrfdQAdHMSSFYfxaTjRKH+PwQ6crgBVaykGK622T3oOIG9zBfEtKNw2RVNIZjbB5niSfZk6taOHhUY9qB7Iq3UQU5SN7qAbIJZ+fzK2U1W2cIR49n48kjVa2Nz7jarvcPKSjuyLm9CSONoXePpRFtQP4G2nEk86Nozf0421U6R6dyGs6a//NzKQ6j5NIg/MXtxjxHUCiJg0MEc7aRmjfa+rkU0cEfijEcKgYgZYiFeRipnvyXcyjZErZ9tjhOCTAAzLFqzz+kWboAAAAASUVORK5CYII="
                               }, format='json')
        # print response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['detail'], 'incident_does_not_exists')

    def testMediaIncidentResortNotEqualUserResort(self):
        """
        Purpose - Test POST media with different incident resort than user resort
        Ticket no - #332
        Date created - 08/14/2015
        Date updated - 08/14/2015
        Updates made:
         -
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testMediaIncidentResortNotEqualUserResort
        """
        # print self.domain.pk
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        # print response.content
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user1.email, 'password': '1234'}, format='json')
        response = self.c.post('/api/v3/incidents/' + str(self.incident.incident_id) + '/media/',
                               {
                                   "mimeType": "image/png",
                                   "media": "iVBORw0KGgoAAAANSUhEUgAAAB8AAAAeCAYAAADU8sWcAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAABQ5JREFUeNqclw1MlVUYx18uN0hGkYWJYFPS3LK6ViS1JX5VmqFpDtFhhrY+wcpMsWzOj+mKghppSiWGmSzXyrIsy0qKyo8MKyKaWRRaimFL0jI/0P/Dfq87u/G1zvbbC+89933O+3/+z3POjVif0NXrwDhbDBXXi1TRV3QSJ/m8QXwttor3uB5v76ER7QQ/X+SI28UF3Nst9vHwf8WZojv4Y4coFGvaWkSwjcA3inwREkdEgXhZ1IrDzDkhIkU0Cx0hpoj+zL1b3Icq/xmBFu5FEuhdAtuYJ2bykEaCnnAWEC8WiF9JywBRIdLEpyK7I8Ht/2LxEA9ayn2TvVsryt2LzJP420admCueEmeIUnFPe8FN5jvELjFa5Ioy0Uc8GjY3FXMtIcDjYqF4SdSIj0Q/8TBpWiYyWwt+i5gh/hC3ii+5PweD2UJG8h0LUk4FfCVuYN4TIkNcJYaJ61DHf+tCx7ing8cjkY0HKBV//CRmOV/ejgp/iywxGIlzeIaVYIrYiEeuxHzPURGPhQe3nPYUq5kYPj4XvyC/Sfk8Eh5E0j0srIZnFGLansz1WKB5YaIY7gePoSQ85+1P9wFKxxzbAxVGMD9WrBdjUWs/ss/he3b/ZpSyUS8W8fckP7jJdqHYJCqdwJci3QrRRTyDQha8RPwg1lERUfjAPHCUUhvNIsucZ77FIs073QK41sZrXGOp2a0Y5kNxLeViQZPFKOYv4zsVGHITJXoehrTGs5YF29grvhBxFteCX8EHn2COCqSz5jENJ28R08n7GHp8L1xtnfBn8YpTSn/R9eJoUCHn7d/mepkF7y124l4zy+XIk0nz8DePRlycIL4R31E2lZSXff49pTpIPEibNbV+F2/ihVqel2DBE8mZ1fJscReBLcjHeMIj5+bszUjaCUdHo8wCpH9VPOsEnC8eYZM56SiQGGRn8nv6BrFS3Elj2E4HS2U3K8CcDahTy65VJS7iaia8SQwRUx2VsinFfcRrCpKfOEyynFxn0WKnUma2oEtEtRhn+RLvsKAJlNpwFlpCddhbH0ChEkp6BwZu3poD1G4XHJ1Kb97FBLs+TestdfpBVzaaeKriajGZN16KURP5/gz8MIW0+gavD2B9j8k72TqTqcX3xYtI/Rv57oWMDZRRkHQNZVebjk9W4ZsXqKJS55xg49sgrdPGQDb+daix32mJh+lWfdj5JtBk8vBBDbLa7laEIjWkY6Njsh4sxCpicwDnWrB0TizJyBhiI6hD7jrqeRi1Xs3ONxNjZlIRMTj8mrDAHs2pM4odCFDfRXw4GwNuoxefI86lJ08jWCnG+gAVFmOkNJ5xEKkbwwInObtjcwoiJ8ZaN21uDhn05B8pD383G8+9Mh6cT7nEcFBIp23eT20PItevhwUvoPxW+S8bcFabx99FSGbjT/KWRo5n0fuHcNy6mK6YwtvMJYVZ+MIfuTSvvajruW/uv30UOU3nrfdQAdHMSSFYfxaTjRKH+PwQ6crgBVaykGK622T3oOIG9zBfEtKNw2RVNIZjbB5niSfZk6taOHhUY9qB7Iq3UQU5SN7qAbIJZ+fzK2U1W2cIR49n48kjVa2Nz7jarvcPKSjuyLm9CSONoXePpRFtQP4G2nEk86Nozf0421U6R6dyGs6a//NzKQ6j5NIg/MXtxjxHUCiJg0MEc7aRmjfa+rkU0cEfijEcKgYgZYiFeRipnvyXcyjZErZ9tjhOCTAAzLFqzz+kWboAAAAASUVORK5CYII="
                               }, format='json')
        # print response
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.content)['detail'],
                         'you_do_not_have_permission_to_add_media_to_this_incident')

    def testMediaMimeTypeNone(self):
        """
        Purpose - Test POST media with invalid mime type
        Ticket no - #332
        Date created - 08/14/2015
        Date updated - 08/14/2015
        Updates made:
         -
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testMediaMimeTypeNone
        """
        # print self.domain.pk
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        # print response.content
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')
        response = self.c.post('/api/v3/incidents/' + str(self.incident.incident_id) + '/media/',
                               {
                                   "media": "iVBORw0KGgoAAAANSUhEUgAAAB8AAAAeCAYAAADU8sWcAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAABQ5JREFUeNqclw1MlVUYx18uN0hGkYWJYFPS3LK6ViS1JX5VmqFpDtFhhrY+wcpMsWzOj+mKghppSiWGmSzXyrIsy0qKyo8MKyKaWRRaimFL0jI/0P/Dfq87u/G1zvbbC+89933O+3/+z3POjVif0NXrwDhbDBXXi1TRV3QSJ/m8QXwttor3uB5v76ER7QQ/X+SI28UF3Nst9vHwf8WZojv4Y4coFGvaWkSwjcA3inwREkdEgXhZ1IrDzDkhIkU0Cx0hpoj+zL1b3Icq/xmBFu5FEuhdAtuYJ2bykEaCnnAWEC8WiF9JywBRIdLEpyK7I8Ht/2LxEA9ayn2TvVsryt2LzJP420admCueEmeIUnFPe8FN5jvELjFa5Ioy0Uc8GjY3FXMtIcDjYqF4SdSIj0Q/8TBpWiYyWwt+i5gh/hC3ii+5PweD2UJG8h0LUk4FfCVuYN4TIkNcJYaJ61DHf+tCx7ing8cjkY0HKBV//CRmOV/ejgp/iywxGIlzeIaVYIrYiEeuxHzPURGPhQe3nPYUq5kYPj4XvyC/Sfk8Eh5E0j0srIZnFGLansz1WKB5YaIY7gePoSQ85+1P9wFKxxzbAxVGMD9WrBdjUWs/ss/he3b/ZpSyUS8W8fckP7jJdqHYJCqdwJci3QrRRTyDQha8RPwg1lERUfjAPHCUUhvNIsucZ77FIs073QK41sZrXGOp2a0Y5kNxLeViQZPFKOYv4zsVGHITJXoehrTGs5YF29grvhBxFteCX8EHn2COCqSz5jENJ28R08n7GHp8L1xtnfBn8YpTSn/R9eJoUCHn7d/mepkF7y124l4zy+XIk0nz8DePRlycIL4R31E2lZSXff49pTpIPEibNbV+F2/ihVqel2DBE8mZ1fJscReBLcjHeMIj5+bszUjaCUdHo8wCpH9VPOsEnC8eYZM56SiQGGRn8nv6BrFS3Elj2E4HS2U3K8CcDahTy65VJS7iaia8SQwRUx2VsinFfcRrCpKfOEyynFxn0WKnUma2oEtEtRhn+RLvsKAJlNpwFlpCddhbH0ChEkp6BwZu3poD1G4XHJ1Kb97FBLs+TestdfpBVzaaeKriajGZN16KURP5/gz8MIW0+gavD2B9j8k72TqTqcX3xYtI/Rv57oWMDZRRkHQNZVebjk9W4ZsXqKJS55xg49sgrdPGQDb+daix32mJh+lWfdj5JtBk8vBBDbLa7laEIjWkY6Njsh4sxCpicwDnWrB0TizJyBhiI6hD7jrqeRi1Xs3ONxNjZlIRMTj8mrDAHs2pM4odCFDfRXw4GwNuoxefI86lJ08jWCnG+gAVFmOkNJ5xEKkbwwInObtjcwoiJ8ZaN21uDhn05B8pD383G8+9Mh6cT7nEcFBIp23eT20PItevhwUvoPxW+S8bcFabx99FSGbjT/KWRo5n0fuHcNy6mK6YwtvMJYVZ+MIfuTSvvajruW/uv30UOU3nrfdQAdHMSSFYfxaTjRKH+PwQ6crgBVaykGK622T3oOIG9zBfEtKNw2RVNIZjbB5niSfZk6taOHhUY9qB7Iq3UQU5SN7qAbIJZ+fzK2U1W2cIR49n48kjVa2Nz7jarvcPKSjuyLm9CSONoXePpRFtQP4G2nEk86Nozf0421U6R6dyGs6a//NzKQ6j5NIg/MXtxjxHUCiJg0MEc7aRmjfa+rkU0cEfijEcKgYgZYiFeRipnvyXcyjZErZ9tjhOCTAAzLFqzz+kWboAAAAASUVORK5CYII="
                               }, format='json')
        # print response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['detail'], 'mimetype_is_required')

    def testMediaMimeTypeInvalid(self):
        """
        Purpose - Test POST media with invalid mime type
        Ticket no - #332
        Date created - 08/15/2015
        Date updated - 08/15/2015
        Updates made:
         -
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testMediaMimeTypeInvalid
        """
        # print self.domain.pk
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        # print response.content
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')
        response = self.c.post('/api/v3/incidents/' + str(self.incident.incident_id) + '/media/',
                               {
                                   "mimeType": "image-png",
                                   "media": "iVBORw0KGgoAAAANSUhEUgAAAB8AAAAeCAYAAADU8sWcAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAABQ5JREFUeNqclw1MlVUYx18uN0hGkYWJYFPS3LK6ViS1JX5VmqFpDtFhhrY+wcpMsWzOj+mKghppSiWGmSzXyrIsy0qKyo8MKyKaWRRaimFL0jI/0P/Dfq87u/G1zvbbC+89933O+3/+z3POjVif0NXrwDhbDBXXi1TRV3QSJ/m8QXwttor3uB5v76ER7QQ/X+SI28UF3Nst9vHwf8WZojv4Y4coFGvaWkSwjcA3inwREkdEgXhZ1IrDzDkhIkU0Cx0hpoj+zL1b3Icq/xmBFu5FEuhdAtuYJ2bykEaCnnAWEC8WiF9JywBRIdLEpyK7I8Ht/2LxEA9ayn2TvVsryt2LzJP420admCueEmeIUnFPe8FN5jvELjFa5Ioy0Uc8GjY3FXMtIcDjYqF4SdSIj0Q/8TBpWiYyWwt+i5gh/hC3ii+5PweD2UJG8h0LUk4FfCVuYN4TIkNcJYaJ61DHf+tCx7ing8cjkY0HKBV//CRmOV/ejgp/iywxGIlzeIaVYIrYiEeuxHzPURGPhQe3nPYUq5kYPj4XvyC/Sfk8Eh5E0j0srIZnFGLansz1WKB5YaIY7gePoSQ85+1P9wFKxxzbAxVGMD9WrBdjUWs/ss/he3b/ZpSyUS8W8fckP7jJdqHYJCqdwJci3QrRRTyDQha8RPwg1lERUfjAPHCUUhvNIsucZ77FIs073QK41sZrXGOp2a0Y5kNxLeViQZPFKOYv4zsVGHITJXoehrTGs5YF29grvhBxFteCX8EHn2COCqSz5jENJ28R08n7GHp8L1xtnfBn8YpTSn/R9eJoUCHn7d/mepkF7y124l4zy+XIk0nz8DePRlycIL4R31E2lZSXff49pTpIPEibNbV+F2/ihVqel2DBE8mZ1fJscReBLcjHeMIj5+bszUjaCUdHo8wCpH9VPOsEnC8eYZM56SiQGGRn8nv6BrFS3Elj2E4HS2U3K8CcDahTy65VJS7iaia8SQwRUx2VsinFfcRrCpKfOEyynFxn0WKnUma2oEtEtRhn+RLvsKAJlNpwFlpCddhbH0ChEkp6BwZu3poD1G4XHJ1Kb97FBLs+TestdfpBVzaaeKriajGZN16KURP5/gz8MIW0+gavD2B9j8k72TqTqcX3xYtI/Rv57oWMDZRRkHQNZVebjk9W4ZsXqKJS55xg49sgrdPGQDb+daix32mJh+lWfdj5JtBk8vBBDbLa7laEIjWkY6Njsh4sxCpicwDnWrB0TizJyBhiI6hD7jrqeRi1Xs3ONxNjZlIRMTj8mrDAHs2pM4odCFDfRXw4GwNuoxefI86lJ08jWCnG+gAVFmOkNJ5xEKkbwwInObtjcwoiJ8ZaN21uDhn05B8pD383G8+9Mh6cT7nEcFBIp23eT20PItevhwUvoPxW+S8bcFabx99FSGbjT/KWRo5n0fuHcNy6mK6YwtvMJYVZ+MIfuTSvvajruW/uv30UOU3nrfdQAdHMSSFYfxaTjRKH+PwQ6crgBVaykGK622T3oOIG9zBfEtKNw2RVNIZjbB5niSfZk6taOHhUY9qB7Iq3UQU5SN7qAbIJZ+fzK2U1W2cIR49n48kjVa2Nz7jarvcPKSjuyLm9CSONoXePpRFtQP4G2nEk86Nozf0421U6R6dyGs6a//NzKQ6j5NIg/MXtxjxHUCiJg0MEc7aRmjfa+rkU0cEfijEcKgYgZYiFeRipnvyXcyjZErZ9tjhOCTAAzLFqzz+kWboAAAAASUVORK5CYII="
                               }, format='json')
        # print response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['detail'], 'invalid_mime_type_provided')

    def testMediaNoneContent(self):
        """
        Purpose - Test POST media with special scenario.
        Ticket no - #332
        Date created - 08/15/2015
        Date updated - 08/15/2015
        Updates made:
         -
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testMediaNoneContent
        """
        # print self.domain.pk
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        # print response.content
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')
        response = self.c.post('/api/v3/incidents/' + str(self.incident.incident_id) + '/media/',
                               {
                                   "mimeType": "image/png"
                               }, format='json')
        # print response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['detail'], 'media_content_not_provided')

    def testMediaInvalidBase64Content(self):
        """
        Purpose - Test POST media with invalid content
        Ticket no - #332
        Date created - 08/15/2015
        Date updated - 08/15/2015
        Updates made:
         -
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testMediaInvalidBase64Content
        """
        # print self.domain.pk
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        # print response.content
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')
        response = self.c.post('/api/v3/incidents/' + str(self.incident.incident_id) + '/media/',
                               {
                                   "mimeType": "image/png",
                                   "media": "---...#ORw0KGgoAAAANSUhEUgAAAB8AAAAeCAYAAADU8sWcAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAABQ5JREFUeNqclw1MlVUYx18uN0hGkYWJYFPS3LK6ViS1JX5VmqFpDtFhhrY+wcpMsWzOj+mKghppSiWGmSzXyrIsy0qKyo8MKyKaWRRaimFL0jI/0P/Dfq87u/G1zvbbC+89933O+3/+z3POjVif0NXrwDhbDBXXi1TRV3QSJ/m8QXwttor3uB5v76ER7QQ/X+SI28UF3Nst9vHwf8WZojv4Y4coFGvaWkSwjcA3inwREkdEgXhZ1IrDzDkhIkU0Cx0hpoj+zL1b3Icq/xmBFu5FEuhdAtuYJ2bykEaCnnAWEC8WiF9JywBRIdLEpyK7I8Ht/2LxEA9ayn2TvVsryt2LzJP420admCueEmeIUnFPe8FN5jvELjFa5Ioy0Uc8GjY3FXMtIcDjYqF4SdSIj0Q/8TBpWiYyWwt+i5gh/hC3ii+5PweD2UJG8h0LUk4FfCVuYN4TIkNcJYaJ61DHf+tCx7ing8cjkY0HKBV//CRmOV/ejgp/iywxGIlzeIaVYIrYiEeuxHzPURGPhQe3nPYUq5kYPj4XvyC/Sfk8Eh5E0j0srIZnFGLansz1WKB5YaIY7gePoSQ85+1P9wFKxxzbAxVGMD9WrBdjUWs/ss/he3b/ZpSyUS8W8fckP7jJdqHYJCqdwJci3QrRRTyDQha8RPwg1lERUfjAPHCUUhvNIsucZ77FIs073QK41sZrXGOp2a0Y5kNxLeViQZPFKOYv4zsVGHITJXoehrTGs5YF29grvhBxFteCX8EHn2COCqSz5jENJ28R08n7GHp8L1xtnfBn8YpTSn/R9eJoUCHn7d/mepkF7y124l4zy+XIk0nz8DePRlycIL4R31E2lZSXff49pTpIPEibNbV+F2/ihVqel2DBE8mZ1fJscReBLcjHeMIj5+bszUjaCUdHo8wCpH9VPOsEnC8eYZM56SiQGGRn8nv6BrFS3Elj2E4HS2U3K8CcDahTy65VJS7iaia8SQwRUx2VsinFfcRrCpKfOEyynFxn0WKnUma2oEtEtRhn+RLvsKAJlNpwFlpCddhbH0ChEkp6BwZu3poD1G4XHJ1Kb97FBLs+TestdfpBVzaaeKriajGZN16KURP5/gz8MIW0+gavD2B9j8k72TqTqcX3xYtI/Rv57oWMDZRRkHQNZVebjk9W4ZsXqKJS55xg49sgrdPGQDb+daix32mJh+lWfdj5JtBk8vBBDbLa7laEIjWkY6Njsh4sxCpicwDnWrB0TizJyBhiI6hD7jrqeRi1Xs3ONxNjZlIRMTj8mrDAHs2pM4odCFDfRXw4GwNuoxefI86lJ08jWCnG+gAVFmOkNJ5xEKkbwwInObtjcwoiJ8ZaN21uDhn05B8pD383G8+9Mh6cT7nEcFBIp23eT20PItevhwUvoPxW+S8bcFabx99FSGbjT/KWRo5n0fuHcNy6mK6YwtvMJYVZ+MIfuTSvvajruW/uv30UOU3nrfdQAdHMSSFYfxaTjRKH+PwQ6crgBVaykGK622T3oOIG9zBfEtKNw2RVNIZjbB5niSfZk6taOHhUY9qB7Iq3UQU5SN7qAbIJZ+fzK2U1W2cIR49n48kjVa2Nz7jarvcPKSjuyLm9CSON........."
                               }, format='json')
        # print response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['detail'], 'base64_string_is_not_valid')

    def testMediaReference(self):
        """
        Purpose - Test POST media with media reference
        Ticket no - #332
        Date created - 08/15/2015
        Date updated - 08/15/2015
        Updates made:
         -
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testMediaReference
        """
        # print self.domain.pk
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        # print response.content
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')
        response = self.c.post('/api/v3/incidents/' + str(self.incident.incident_id) + '/media/',
                               {
                                   "mimeType": "image/png",
                                   "media_reference": "new-reference-test1",
                                   "media": "iVBORw0KGgoAAAANSUhEUgAAAB8AAAAeCAYAAADU8sWcAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAABQ5JREFUeNqclw1MlVUYx18uN0hGkYWJYFPS3LK6ViS1JX5VmqFpDtFhhrY+wcpMsWzOj+mKghppSiWGmSzXyrIsy0qKyo8MKyKaWRRaimFL0jI/0P/Dfq87u/G1zvbbC+89933O+3/+z3POjVif0NXrwDhbDBXXi1TRV3QSJ/m8QXwttor3uB5v76ER7QQ/X+SI28UF3Nst9vHwf8WZojv4Y4coFGvaWkSwjcA3inwREkdEgXhZ1IrDzDkhIkU0Cx0hpoj+zL1b3Icq/xmBFu5FEuhdAtuYJ2bykEaCnnAWEC8WiF9JywBRIdLEpyK7I8Ht/2LxEA9ayn2TvVsryt2LzJP420admCueEmeIUnFPe8FN5jvELjFa5Ioy0Uc8GjY3FXMtIcDjYqF4SdSIj0Q/8TBpWiYyWwt+i5gh/hC3ii+5PweD2UJG8h0LUk4FfCVuYN4TIkNcJYaJ61DHf+tCx7ing8cjkY0HKBV//CRmOV/ejgp/iywxGIlzeIaVYIrYiEeuxHzPURGPhQe3nPYUq5kYPj4XvyC/Sfk8Eh5E0j0srIZnFGLansz1WKB5YaIY7gePoSQ85+1P9wFKxxzbAxVGMD9WrBdjUWs/ss/he3b/ZpSyUS8W8fckP7jJdqHYJCqdwJci3QrRRTyDQha8RPwg1lERUfjAPHCUUhvNIsucZ77FIs073QK41sZrXGOp2a0Y5kNxLeViQZPFKOYv4zsVGHITJXoehrTGs5YF29grvhBxFteCX8EHn2COCqSz5jENJ28R08n7GHp8L1xtnfBn8YpTSn/R9eJoUCHn7d/mepkF7y124l4zy+XIk0nz8DePRlycIL4R31E2lZSXff49pTpIPEibNbV+F2/ihVqel2DBE8mZ1fJscReBLcjHeMIj5+bszUjaCUdHo8wCpH9VPOsEnC8eYZM56SiQGGRn8nv6BrFS3Elj2E4HS2U3K8CcDahTy65VJS7iaia8SQwRUx2VsinFfcRrCpKfOEyynFxn0WKnUma2oEtEtRhn+RLvsKAJlNpwFlpCddhbH0ChEkp6BwZu3poD1G4XHJ1Kb97FBLs+TestdfpBVzaaeKriajGZN16KURP5/gz8MIW0+gavD2B9j8k72TqTqcX3xYtI/Rv57oWMDZRRkHQNZVebjk9W4ZsXqKJS55xg49sgrdPGQDb+daix32mJh+lWfdj5JtBk8vBBDbLa7laEIjWkY6Njsh4sxCpicwDnWrB0TizJyBhiI6hD7jrqeRi1Xs3ONxNjZlIRMTj8mrDAHs2pM4odCFDfRXw4GwNuoxefI86lJ08jWCnG+gAVFmOkNJ5xEKkbwwInObtjcwoiJ8ZaN21uDhn05B8pD383G8+9Mh6cT7nEcFBIp23eT20PItevhwUvoPxW+S8bcFabx99FSGbjT/KWRo5n0fuHcNy6mK6YwtvMJYVZ+MIfuTSvvajruW/uv30UOU3nrfdQAdHMSSFYfxaTjRKH+PwQ6crgBVaykGK622T3oOIG9zBfEtKNw2RVNIZjbB5niSfZk6taOHhUY9qB7Iq3UQU5SN7qAbIJZ+fzK2U1W2cIR49n48kjVa2Nz7jarvcPKSjuyLm9CSONoXePpRFtQP4G2nEk86Nozf0421U6R6dyGs6a//NzKQ6j5NIg/MXtxjxHUCiJg0MEc7aRmjfa+rkU0cEfijEcKgYgZYiFeRipnvyXcyjZErZ9tjhOCTAAzLFqzz+kWboAAAAASUVORK5CYII="
                               }, format='json')
        # print response
        self.assertEqual(response.status_code, 200)

    def testMediaReferenceInvalid(self):
        """
        Purpose - Test POST media with media reference
        Ticket no - #332
        Date created - 08/15/2015
        Date updated - 08/15/2015
        Updates made:
         -
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.testMediaReferenceInvalid
        """
        # print self.domain.pk
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        # print response.content
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')
        response = self.c.post('/api/v3/incidents/' + str(self.incident.incident_id) + '/media/',
                               {
                                   "mimeType": "image/png",
                                   "media_reference": "new-reference-test1",
                                   "media": "iVBORw0KGgoAAAANSUhEUgAAAB8AAAAeCAYAAADU8sWcAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAABQ5JREFUeNqclw1MlVUYx18uN0hGkYWJYFPS3LK6ViS1JX5VmqFpDtFhhrY+wcpMsWzOj+mKghppSiWGmSzXyrIsy0qKyo8MKyKaWRRaimFL0jI/0P/Dfq87u/G1zvbbC+89933O+3/+z3POjVif0NXrwDhbDBXXi1TRV3QSJ/m8QXwttor3uB5v76ER7QQ/X+SI28UF3Nst9vHwf8WZojv4Y4coFGvaWkSwjcA3inwREkdEgXhZ1IrDzDkhIkU0Cx0hpoj+zL1b3Icq/xmBFu5FEuhdAtuYJ2bykEaCnnAWEC8WiF9JywBRIdLEpyK7I8Ht/2LxEA9ayn2TvVsryt2LzJP420admCueEmeIUnFPe8FN5jvELjFa5Ioy0Uc8GjY3FXMtIcDjYqF4SdSIj0Q/8TBpWiYyWwt+i5gh/hC3ii+5PweD2UJG8h0LUk4FfCVuYN4TIkNcJYaJ61DHf+tCx7ing8cjkY0HKBV//CRmOV/ejgp/iywxGIlzeIaVYIrYiEeuxHzPURGPhQe3nPYUq5kYPj4XvyC/Sfk8Eh5E0j0srIZnFGLansz1WKB5YaIY7gePoSQ85+1P9wFKxxzbAxVGMD9WrBdjUWs/ss/he3b/ZpSyUS8W8fckP7jJdqHYJCqdwJci3QrRRTyDQha8RPwg1lERUfjAPHCUUhvNIsucZ77FIs073QK41sZrXGOp2a0Y5kNxLeViQZPFKOYv4zsVGHITJXoehrTGs5YF29grvhBxFteCX8EHn2COCqSz5jENJ28R08n7GHp8L1xtnfBn8YpTSn/R9eJoUCHn7d/mepkF7y124l4zy+XIk0nz8DePRlycIL4R31E2lZSXff49pTpIPEibNbV+F2/ihVqel2DBE8mZ1fJscReBLcjHeMIj5+bszUjaCUdHo8wCpH9VPOsEnC8eYZM56SiQGGRn8nv6BrFS3Elj2E4HS2U3K8CcDahTy65VJS7iaia8SQwRUx2VsinFfcRrCpKfOEyynFxn0WKnUma2oEtEtRhn+RLvsKAJlNpwFlpCddhbH0ChEkp6BwZu3poD1G4XHJ1Kb97FBLs+TestdfpBVzaaeKriajGZN16KURP5/gz8MIW0+gavD2B9j8k72TqTqcX3xYtI/Rv57oWMDZRRkHQNZVebjk9W4ZsXqKJS55xg49sgrdPGQDb+daix32mJh+lWfdj5JtBk8vBBDbLa7laEIjWkY6Njsh4sxCpicwDnWrB0TizJyBhiI6hD7jrqeRi1Xs3ONxNjZlIRMTj8mrDAHs2pM4odCFDfRXw4GwNuoxefI86lJ08jWCnG+gAVFmOkNJ5xEKkbwwInObtjcwoiJ8ZaN21uDhn05B8pD383G8+9Mh6cT7nEcFBIp23eT20PItevhwUvoPxW+S8bcFabx99FSGbjT/KWRo5n0fuHcNy6mK6YwtvMJYVZ+MIfuTSvvajruW/uv30UOU3nrfdQAdHMSSFYfxaTjRKH+PwQ6crgBVaykGK622T3oOIG9zBfEtKNw2RVNIZjbB5niSfZk6taOHhUY9qB7Iq3UQU5SN7qAbIJZ+fzK2U1W2cIR49n48kjVa2Nz7jarvcPKSjuyLm9CSONoXePpRFtQP4G2nEk86Nozf0421U6R6dyGs6a//NzKQ6j5NIg/MXtxjxHUCiJg0MEc7aRmjfa+rkU0cEfijEcKgYgZYiFeRipnvyXcyjZErZ9tjhOCTAAzLFqzz+kWboAAAAASUVORK5CYII="
                               }, format='json')
        # print response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['detail'], 'media_reference_not_found_in_incident')

    def newDataTypeTest(self):
        """
        Purpose - Testing new data type temperature, weight, height, distance, patient_age, distance,length, altitude
        Ticket no - #408
        Date created - 24/01/2016
        Date updated - 24/01/2016
        Updates made:
         -
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase.newDataTypeTest
        """
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        custom_imcident_json = FULL_INCIDENT_JSON
        custom_imcident_json.update({
            "field_52ca461ccc0fd": 25.7,
            "field_52ca4637cc0fe": 56.5,
            "field_52dd8bee9b004": 569,
            "field_52dd8c049b005": 26,
            "patient_age": 18
        })

        response = self.c.post('/api/v3/incidents/',
                               custom_imcident_json, format='json')
        self.assertEqual(response.status_code, 200)

        # Temprature and distance more than one digit after decimal point
        custom_imcident_json.update({
            "field_52ca461ccc0fd": 25.7565,
            "field_52ca4637cc0fe": 56.5656,
            "field_52dd8bee9b004": 569,
            "field_52dd8c049b005": 26,
            "patient_age": 18
        })
        response = self.c.post('/api/v3/incidents/',
                               custom_imcident_json, format='json')
        self.assertEqual(json.loads(response.content), {"field_52ca461ccc0fd": "must be single decimal place",
                                                        "field_52ca4637cc0fe": "must be single decimal place"})

        # Float value for weight, height, patient_age
        custom_imcident_json.update({
            "field_52ca461ccc0fd": 25.7,
            "field_52ca4637cc0fe": 56.5,
            "field_52dd8bee9b004": 569.3,
            "field_52dd8c049b005": 26.4,
            "patient_age": 18.6
        })
        response = self.c.post('/api/v3/incidents/',
                               custom_imcident_json, format='json')
        self.assertEqual(json.loads(response.content),
                         {'field_52dd8bee9b004': 'must be integer', 'field_52dd8c049b005': 'must be integer',
                          'patient_age': 'must be int'})

        # Float value for weight, height, patient_age
        custom_imcident_json.update({
            "field_52ca461ccc0fd": "some value",
            "field_52ca4637cc0fe": "some value",
            "field_52dd8bee9b004": "some value",
            "field_52dd8c049b005": "some value",
            "patient_age": "some value"
        })
        response = self.c.post('/api/v3/incidents/',
                               custom_imcident_json, format='json')
        self.assertEqual(json.loads(response.content),
                         {'field_52ca461ccc0fd': 'must be float',
                          'field_52ca4637cc0fe': 'must be float',
                          'field_52dd8bee9b004': 'must be integer',
                          'field_52dd8c049b005': 'must be integer',
                          'patient_age': 'must be int'})


class UserConnectedTestCase(APITestCase):
    def setUp(self):
        self.solo_user = UserFactory()  # user_connected = SOLO by defaut.
        self.network_user = UserFactory(email='user2@admin.com', name="User2",
                                        user_connected=1)  # user_connected = Network
        self.application = ApplicationFactory()
        self.incidentTemplate = IncidentTemplateFactory(template_id=1)
        self.domain = DomainFactory(domain_id=1, domain='api-dev-us.medic52.com')
        self.domain = DomainFactory(domain='api-dev-au.medic52.com', is_active=True)
        self.domain = DomainFactory(domain='testserver', is_active=True)
        self.resort = ResortFactory(domain_id=self.domain)
        self.userRoles = UserRolesFactory(role_id=3, key='manager', order=3)
        self.user_resort_map = UserResortMapFactory(user=self.solo_user, resort=self.resort, role_id=3)
        self.network_user_resort_map = UserResortMapFactory(user=self.network_user, resort=self.resort, role_id=3)
        self.incidentStatus = IncidentStatusFactory(incident_status_id=1)
        self.incidentStatus2 = IncidentStatusFactory(incident_status_id=2, key="status2")

        self.c = APIClient()
        self.token = TokenFactory(user=self.solo_user)

    def testMobileSoloUserIncidents(self):
        """
        Purpose - Tests to check solo user on resort not shown in networked user list
        Ticket no - #304
        Date created - 07/20/2015
        Date updated - 07/21/2015
        Updates made:
         - Tests to check solo user on resort not shown in networked user list
        Additional comment:
         - Tests to check solo user on resort not shown in networked user list
        command:
         - python manage.py test apps.incidents.tests.UserConnectedTestCase.testMobileSoloUserIncidents
        """
        from django.db import connection

        with connection.cursor() as c:
            c.execute(
                'GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO %s; CREATE EXTENSION IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";' %
                settings.DATABASES['default']['USER'])

        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.solo_user.email, 'password': '1234'},
                               format='json')

        incident_json = {
            "name": "Gary Barlow",
            "email": "garry@barrlow.com",
            "phone": "+50672514236",
            "dob": "1978-07-15",
            "sex": "male",
            "address": "5th Avenue, San Diego",
            "suburb": "Los Ranchos",
            "state": "California",
            "country": "United States",
            "postcode": "12152"
        }

        for i in range(0, 4):
            response = self.c.post('/api/v3/incidents/',
                                   incident_json, format='json')
            self.assertEqual(response.status_code, 200)

        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user.email, 'password': '1234'},
                               format='json')

        for i in range(0, 4):
            response = self.c.post('/api/v3/incidents/',
                                   incident_json, format='json')
            self.assertEqual(response.status_code, 200)

        response = self.c.get('/api/v3/incidents/?offset=0&chunk=10&resort_id=%s&date_from=%s' % (
            str(self.resort.resort_id), date.today().strftime("%Y-%m-%d 00:00:01")),
                              {}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['count'], 4)
        self.assertEqual(json.loads(response.content)['results'][0]['assigned_to']['name'], "User2")


class OrderByTestCase(APITestCase):
    def setUp(self):
        self.solo_user = UserFactory()  # user_connected = SOLO by defaut.
        self.network_usera = UserFactory(email='user_sort_1@admin.com', name="Auser",
                                         user_connected=1)  # user_connected = Network
        self.network_userb = UserFactory(email='user_sort_2@admin.com', name="Buser",
                                         user_connected=1)  # user_connected = Network
        self.application = ApplicationFactory()
        self.incidentTemplate = IncidentTemplateFactory(template_id=1)
        self.domain = DomainFactory(domain_id=1, domain='api-dev-us.medic52.com')
        self.domain = DomainFactory(domain='api-dev-au.medic52.com', is_active=True)
        self.domain = DomainFactory(domain='testserver', is_active=True)
        self.resort = ResortFactory(domain_id=self.domain)
        self.userRoles = UserRolesFactory(role_id=3, key='manager', order=3)
        self.network_user_resort_map = UserResortMapFactory(user=self.network_usera, resort=self.resort, role_id=3)
        self.network_user_resort_map = UserResortMapFactory(user=self.network_userb, resort=self.resort, role_id=3)
        self.incidentStatus = IncidentStatusFactory()
        self.incidentStatus2 = IncidentStatusFactory(order=2, key="status2")

        self.c = APIClient()
        self.token = TokenFactory(user=self.solo_user)

    def testOderByIncidents(self):
        """
        Purpose - TEST add ordering to list incidents
        Ticket no - #320
        Date created - 07/20/2015
        Date updated - 07/21/2015
        Updates made:
         - TEST add ordering to list incidents
        Additional comment:
         - TEST add ordering to list incidents
        command:
         - python manage.py test apps.incidents.tests.OrderByTestCase.testOderByIncidents
        """
        from django.db import connection

        with connection.cursor() as c:

            c.execute(
                'GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO %s; CREATE EXTENSION IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";' %
                settings.DATABASES['default']['USER'])

        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        # print response.content
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_usera.email, 'password': '1234'},
                               format='json')

        incident_json = {
            "name": "Gary Barlow",
            "email": "garry@barrlow.com",
            "phone": "+50672514236",
            "dob": "1978-07-15",
            "sex": "male",
            "address": "5th Avenue, San Diego",
            "suburb": "Los Ranchos",
            "state": "California",
            "country": "United States",
            "postcode": "12152"
        }

        next_statusa = 1
        next_statusb = 1
        userb_next = False
        created_datetime = datetime.datetime.today()
        for i in range(0, 6):
            if userb_next:
                # Create incidents for user "b"
                response = self.c.post('/api/v3/auth/login/', {'email': self.network_userb.email, 'password': '1234'},
                                       format='json')
            else:
                response = self.c.post('/api/v3/auth/login/', {'email': self.network_usera.email, 'password': '1234'},
                                       format='json')
            create_dt_json = {'dt_created': created_datetime.strftime("%Y-%m-%d %H:%M:%S")}
            response = self.c.post('/api/v3/incidents/',
                                   incident_json, format='json')
            self.assertEqual(response.status_code, 200)
            incident_id = json.loads(response.content)['incident_id']
            response = self.c.put('/api/v3/incidents/%s/' % incident_id,
                                  create_dt_json, format='json')
            self.assertEqual(response.status_code, 200)
            response = self.c.post('/api/v3/incidents/%s/status/' % incident_id,
                                   {"status_type_id": (next_statusb if userb_next else next_statusa),
                                    "status_date": date.today().strftime("%Y-%m-%d %H:%M:%S"),
                                    "updated_by": self.network_usera.user_id}, format='json')
            self.assertEqual(response.status_code, 200)

            if userb_next:
                next_statusb = 2 if next_statusb == 1 else 1
            else:
                next_statusa = 2 if next_statusa == 1 else 1

            userb_next = not userb_next
            created_datetime = created_datetime + timedelta(seconds=-3)

        # ASC
        response = self.c.get('/api/v3/incidents/?order_by=%s&order_by_direction=%s' % ("incident_pk", 'asc'),
                              {}, format='json')
        self.assertEqual(response.status_code, 200)
        sorted_list = json.loads(response.content)['results']
        self.assertGreater(sorted_list[1]['incident_pk'], sorted_list[0]['incident_pk'], "Not Sorted.")
        self.assertGreater(sorted_list[2]['incident_pk'], sorted_list[1]['incident_pk'], "Not Sorted.")

        response = self.c.get('/api/v3/incidents/?order_by=%s&order_by_direction=%s' % ("assigned_to__name", 'asc'),
                              {}, format='json')
        self.assertEqual(response.status_code, 200)
        sorted_list = json.loads(response.content)['results']
        self.assertEqual(sorted_list[0]['assigned_to']['name'], "Auser", "Not Sorted.")
        self.assertEqual(sorted_list[3]['assigned_to']['name'], "Buser", "Not Sorted.")

        response = self.c.get('/api/v3/incidents/?order_by=%s&order_by_direction=%s' % ("dt_created", 'asc'),
                              {}, format='json')
        self.assertEqual(response.status_code, 200)
        sorted_list = json.loads(response.content)['results']
        self.assertGreater(sorted_list[1]['dt_created'], sorted_list[0]['dt_created'], "Not Sorted.")
        self.assertGreater(sorted_list[2]['dt_created'], sorted_list[1]['dt_created'], "Not Sorted.")

        response = self.c.get('/api/v3/incidents/?order_by=%s&order_by_direction=%s' % ("incident_status", 'asc'),
                              {}, format='json')
        self.assertEqual(response.status_code, 200)
        sorted_list = json.loads(response.content)['results']
        self.assertEqual(sorted_list[0]['incident_status'][0]['value'], 1, "Not Sorted.")

        # DESC
        response = self.c.get('/api/v3/incidents/?order_by=%s&order_by_direction=%s' % ("incident_pk", 'desc'),
                              {}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 200)
        sorted_list = json.loads(response.content)['results']
        self.assertGreater(sorted_list[0]['incident_pk'], sorted_list[1]['incident_pk'], "Not Sorted.")
        self.assertGreater(sorted_list[1]['incident_pk'], sorted_list[2]['incident_pk'], "Not Sorted.")

        response = self.c.get('/api/v3/incidents/?order_by=%s&order_by_direction=%s' % ("assigned_to__name", 'desc'),
                              {}, format='json')
        self.assertEqual(response.status_code, 200)
        sorted_list = json.loads(response.content)['results']
        self.assertEqual(sorted_list[0]['assigned_to']['name'], "Buser", "Not Sorted.")
        self.assertEqual(sorted_list[3]['assigned_to']['name'], "Auser", "Not Sorted.")

        response = self.c.get('/api/v3/incidents/?order_by=%s&order_by_direction=%s' % ("dt_created", 'desc'),
                              {}, format='json')
        self.assertEqual(response.status_code, 200)
        sorted_list = json.loads(response.content)['results']
        self.assertGreater(sorted_list[0]['dt_created'], sorted_list[1]['dt_created'], "Not Sorted.")
        self.assertGreater(sorted_list[1]['dt_created'], sorted_list[2]['dt_created'], "Not Sorted.")

        response = self.c.get('/api/v3/incidents/?order_by=%s&order_by_direction=%s' % ("incident_status", 'desc'),
                              {}, format='json')
        self.assertEqual(response.status_code, 200)
        sorted_list = json.loads(response.content)['results']
        self.assertEqual(sorted_list[0]['incident_status'][0]['value'], 2, "Not Sorted.")


class IncidentsTestCase2(APITestCase):
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

    @staticmethod
    def createIncidentStatus():
        incident_status = [[1, 'ff0000', 'call_received'], [2, 'ff0000', 'assigned'], [3, '00ff00', 'on_scene'],
                           [4, '00ff00', 'transport_started'], [5, '00ff00', 'arrived_at_base_clinic'],
                           [6, 'cccccc', 'departure_from_base_clinic'], [7, 'cccccc', 'pending_documentation'],
                           [8, 'ffff', 'case_closed'], [9, 'ffff', 'deleted']]
        incidentStatus = {}
        for status in incident_status:
            incidentStatus[status[0]] = IncidentStatusFactory(incident_status_id=status[0], order=status[0],
                                                              color=status[1], key=status[2])
        return incidentStatus

    def setUp(self):
        self.user = UserFactory(user_connected=1, is_active=True)
        self.userPatroller = UserFactory(email='patroller@yahoo.com', name='Mr Patroller',
                                         user_connected=1, is_active=True)
        self.userDispatcher = UserFactory(email='dispatcher@yahoo.com', name='Mr Dispatcher',
                                          user_connected=1, is_active=True)
        self.application = ApplicationFactory()
        self.incidentTemplate = IncidentTemplateFactory(template_id=1)
        self.domain = DomainFactory(domain_id=1)
        self.domain = DomainFactory(domain='api-dev-au.medic52.com', is_active=True)
        self.domain = DomainFactory(domain='testserver', is_active=True)
        self.resort = ResortFactory(domain_id=self.domain)
        self.userRolePatroller = UserRolesFactory(role_id=1, key='patroller', order=1)
        self.userRoleDispatcher = UserRolesFactory(role_id=2, key='dispatcher', order=2)
        self.userRoleManager = UserRolesFactory(role_id=3, key='manager', order=3)
        self.userResortMapPatroller = UserResortMapFactory(role_id=self.userRolePatroller.role_id,
                                                           user=self.user, resort=self.resort)
        self.userResortMapDispatcher = UserResortMapFactory(role_id=self.userRoleDispatcher.role_id,
                                                            user=self.userDispatcher, resort=self.resort)
        self.userResortMapManager = UserResortMapFactory(role_id=self.userRoleManager.role_id,
                                                         user=self.user, resort=self.resort)
        # create and set incident status
        self.incidentStatus = self.createIncidentStatus()

        self.incident = IncidentFactory(resort=self.resort, assigned_to=self.user,
                                        incident_status=self.incidentStatus[1])
        self.c = APIClient()
        self.token = TokenFactory(user=self.user)

        from django.db import connection

        with connection.cursor() as c:
            c.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')

    def testFileSecurityMedia(self):
        """
        Purpose - Test for checking file security media
        Ticket no - #163
        Date created - 07/06/2015
        Date updated - 07/06/2015
        Updates made:
         - Check if submitted and retrieve data are equal
         - Check if media url is protected in public
        Additional comment:
         - Check uploaded file instead of response due to url redirect to nginx web server
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase2.testFileSecurityMedia
        """
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')
        media_json = {
            "mimeType": "image/png",
            "media": "iVBORw0KGgoAAAANSUhEUgAAAB8AAAAeCAYAAADU8sWcAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAABQ5JREFUeNqclw1MlVUYx18uN0hGkYWJYFPS3LK6ViS1JX5VmqFpDtFhhrY+wcpMsWzOj+mKghppSiWGmSzXyrIsy0qKyo8MKyKaWRRaimFL0jI/0P/Dfq87u/G1zvbbC+89933O+3/+z3POjVif0NXrwDhbDBXXi1TRV3QSJ/m8QXwttor3uB5v76ER7QQ/X+SI28UF3Nst9vHwf8WZojv4Y4coFGvaWkSwjcA3inwREkdEgXhZ1IrDzDkhIkU0Cx0hpoj+zL1b3Icq/xmBFu5FEuhdAtuYJ2bykEaCnnAWEC8WiF9JywBRIdLEpyK7I8Ht/2LxEA9ayn2TvVsryt2LzJP420admCueEmeIUnFPe8FN5jvELjFa5Ioy0Uc8GjY3FXMtIcDjYqF4SdSIj0Q/8TBpWiYyWwt+i5gh/hC3ii+5PweD2UJG8h0LUk4FfCVuYN4TIkNcJYaJ61DHf+tCx7ing8cjkY0HKBV//CRmOV/ejgp/iywxGIlzeIaVYIrYiEeuxHzPURGPhQe3nPYUq5kYPj4XvyC/Sfk8Eh5E0j0srIZnFGLansz1WKB5YaIY7gePoSQ85+1P9wFKxxzbAxVGMD9WrBdjUWs/ss/he3b/ZpSyUS8W8fckP7jJdqHYJCqdwJci3QrRRTyDQha8RPwg1lERUfjAPHCUUhvNIsucZ77FIs073QK41sZrXGOp2a0Y5kNxLeViQZPFKOYv4zsVGHITJXoehrTGs5YF29grvhBxFteCX8EHn2COCqSz5jENJ28R08n7GHp8L1xtnfBn8YpTSn/R9eJoUCHn7d/mepkF7y124l4zy+XIk0nz8DePRlycIL4R31E2lZSXff49pTpIPEibNbV+F2/ihVqel2DBE8mZ1fJscReBLcjHeMIj5+bszUjaCUdHo8wCpH9VPOsEnC8eYZM56SiQGGRn8nv6BrFS3Elj2E4HS2U3K8CcDahTy65VJS7iaia8SQwRUx2VsinFfcRrCpKfOEyynFxn0WKnUma2oEtEtRhn+RLvsKAJlNpwFlpCddhbH0ChEkp6BwZu3poD1G4XHJ1Kb97FBLs+TestdfpBVzaaeKriajGZN16KURP5/gz8MIW0+gavD2B9j8k72TqTqcX3xYtI/Rv57oWMDZRRkHQNZVebjk9W4ZsXqKJS55xg49sgrdPGQDb+daix32mJh+lWfdj5JtBk8vBBDbLa7laEIjWkY6Njsh4sxCpicwDnWrB0TizJyBhiI6hD7jrqeRi1Xs3ONxNjZlIRMTj8mrDAHs2pM4odCFDfRXw4GwNuoxefI86lJ08jWCnG+gAVFmOkNJ5xEKkbwwInObtjcwoiJ8ZaN21uDhn05B8pD383G8+9Mh6cT7nEcFBIp23eT20PItevhwUvoPxW+S8bcFabx99FSGbjT/KWRo5n0fuHcNy6mK6YwtvMJYVZ+MIfuTSvvajruW/uv30UOU3nrfdQAdHMSSFYfxaTjRKH+PwQ6crgBVaykGK622T3oOIG9zBfEtKNw2RVNIZjbB5niSfZk6taOHhUY9qB7Iq3UQU5SN7qAbIJZ+fzK2U1W2cIR49n48kjVa2Nz7jarvcPKSjuyLm9CSONoXePpRFtQP4G2nEk86Nozf0421U6R6dyGs6a//NzKQ6j5NIg/MXtxjxHUCiJg0MEc7aRmjfa+rkU0cEfijEcKgYgZYiFeRipnvyXcyjZErZ9tjhOCTAAzLFqzz+kWboAAAAASUVORK5CYII="
        }
        response = self.c.post('/api/v3/incidents/' + str(self.incident.incident_id) + '/media/',
                               media_json, format='json')
        self.assertEqual(response.status_code, 200)
        media_url = response.data['media_url']
        response = self.c.get(media_url, {}, format='json')
        media_file = os.path.join(settings.MEDIA_ROOT, response['X-Accel-Redirect'].lstrip("/"))
        with open(media_file, 'rb') as incident_file:
            media_content = base64.encodestring(incident_file.read())
            media_content = "".join(media_content.splitlines())
            incident_file.close()
        self.assertEqual(media_content, media_json['media'])
        self.d = APIClient()
        response = self.d.get(media_url, {}, format='json')
        response_json = json.loads(response.content)
        self.assertEqual(response_json['detail'], 'authentication_credentials_were_not_provided')

    def testCreateIncident(self):
        """
        Purpose - Test create incident with fields of null values
        Ticket no - #283
        Date created - 07/05/2015
        Date updated - 07/13/2015
        Updates made:
         - Create incident with null fields
        Additional comment:
         - Create incident with null fields
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase2.testCreateIncident
        """
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')
        incident_json_null = self.incident_json.copy()
        incident_json_null['field_52d47a654d1bb'] = None
        response = self.c.post('/api/v3/incidents/', data=json.dumps(incident_json_null),
                               content_type='application/json')
        response = self.c.get('/api/v3/incidents/' + str(response.data['incident_id']) + '/', format='json')
        response_json = json.loads(response.content)
        self.assertEqual(response.data['field_52d47a654d1bb'], None)

    def testDeletedCases(self):
        """
        Purpose - Test deleted cases
        Ticket no - #301
        Date created - 07/15/2015
        Date updated - 07/20/2015
        Updates made:
         - Test if case is deleted it is not shown in list incidents API's
         - Updated to use assertEqual instead assertContains and transferred to apps.incidents.tests.IncidentsTestCase2
        Additional comment:
         - Test if case is deleted it is not shown in list incidents API's
        command:
         - python manage.py test apps.incidents.tests.IncidentsTestCase2.testDeletedCases
        """
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')
        date_now = datetime.datetime.now()
        # create incident using api
        response = self.c.post('/api/v3/incidents/', data=json.dumps(self.incident_json),
                               content_type='application/json')
        incident_id = str(response.data['incident_id'])
        # get list of incidents using api
        response = self.c.get('/api/v3/incidents/',
                              {
                                  "offset": 0,
                                  "chunk": 3,
                                  "resort_id": str(self.resort.resort_id),
                                  "date_from": date_now.strftime('%Y-%m-%d %H:%M:%S')
                              }, format='json')
        # check response if incident_id exist in list of incidents api
        self.assertEqual(response.data['results'][0]['incident_id'], incident_id)
        # update status of incident to deleted
        response = self.c.post('/api/v3/incidents/' + incident_id + '/status/',
                               {
                                   "status_type_id": self.incidentStatus[9].incident_status_id,
                                   "status_date": date_now.strftime('%Y-%m-%d %H:%M:%S'),
                                   "updated_by": str(self.user.user_id)
                               }, format='json')
        # get list of incidents using api again
        response = self.c.get('/api/v3/incidents/',
                              {
                                  "offset": 0,
                                  "chunk": 3,
                                  "resort_id": str(self.resort.resort_id),
                                  "date_from": date_now.strftime('%Y-%m-%d %H:%M:%S')
                              }, format='json')
        # response must not contain deleted case of incident in list incident api
        self.assertEqual(response.data['count'], 0)


class PrintIncidentTestCase(APITestCase):
    def setUp(self):
        self.network_user = UserFactory(email='user_net@admin.com', name="Auser",
                                        user_connected=1)  # user_connected = Network
        self.network_user_invalid_tz = UserFactory(email='user_net_inv_tz@test.com', name="user1",
                                                   user_connected=1)  # user_connected = Network
        self.application = ApplicationFactory()
        self.incidentTemplate = IncidentTemplateFactory(template_id=1)
        self.domain = DomainFactory(domain_id=1, domain='api-dev-us.medic52.com')
        self.domain = DomainFactory(domain='api-dev-au.medic52.com', is_active=True)
        self.domain = DomainFactory(domain='testserver', is_active=True)
        self.resort = ResortFactory(domain_id=self.domain)
        self.resortInvalidTZ = ResortFactory(resort_name='invalid TZ resort', domain_id=self.domain, timezone='lalala',
                                             network_key='kLoIh67')
        self.userRoles = UserRolesFactory(role_id=3, key='manager', order=3)
        self.network_user_resort_map = UserResortMapFactory(user=self.network_user, resort=self.resort, role_id=3)
        self.network_user_resort_map1 = UserResortMapFactory(user=self.network_user_invalid_tz,
                                                             resort=self.resortInvalidTZ, role_id=3)
        self.incidentStatus = IncidentStatusFactory(incident_status_id=1, key="New Status Test 1")

        self.c = APIClient()
        self.token = TokenFactory(user=self.network_user)

    def testPrintIncidents(self):
        """
        Purpose - Code coverage
        Ticket no - #332
        Date created - 08/03/2015
        Date updated - 08/03/2015
        Updates made:
         -
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.PrintIncidentTestCase.testPrintIncidents
        """
        from django.db import connection

        with connection.cursor() as c:
            c.execute(
                'GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO %s; CREATE EXTENSION IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";' %
                settings.DATABASES['default']['USER'])

        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        # print response.content
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user.email, 'password': '1234'},
                               format='json')

        incident_json = {
            "name": "Gary Barlow",
            "email": "garry@barrlow.com",
            "phone": "+50672514236",
            "dob": "1978-07-15",
            "sex": "male",
            "address": "5th Avenue, San Diego",
            "suburb": "Los Ranchos",
            "state": "California",
            "country": "United States",
            "postcode": "12152"
        }

        response = self.c.post('/api/v3/incidents/',
                               incident_json, format='json')
        self.assertEqual(response.status_code, 200)
        incident_id = json.loads(response.content)['incident_id']
        print_response = self.c.get('/api/v3/incidents/%s/print/' % incident_id,
                                    {}, format='json')
        self.assertEqual(print_response.status_code, 200)

    def testPrintInvalidResortTimezone(self):
        """
        Purpose - Code coverage
        Ticket no - #332
        Date created - 08/17/2015
        Date updated - 08/17/2015
        Updates made:
         -
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.PrintIncidentTestCase.testPrintInvalidResortTimezone
        """
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        # print response.content
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user_invalid_tz.email, 'password': '1234'},
                               format='json')

        incident_json = {
            "name": "Gary Barlow",
            "email": "garry@barrlow.com",
            "phone": "+50672514236",
            "dob": "1978-07-15",
            "sex": "male",
            "address": "5th Avenue, San Diego",
            "suburb": "Los Ranchos",
            "state": "California",
            "country": "United States",
            "postcode": "12152"
        }

        response = self.c.post('/api/v3/incidents/',
                               incident_json, format='json')
        self.assertEqual(response.status_code, 200)
        incident_id = json.loads(response.content)['incident_id']
        print_response = self.c.get('/api/v3/incidents/%s/print/' % incident_id,
                                    {}, format='json')
        self.assertEqual(print_response.status_code, 400)
        self.assertEqual(json.loads(print_response.content)['detail'], "please_set_the_correct_timezone_for_resort")


class IncidentStatusTestCase(APITestCase):
    def setUp(self):
        self.network_user = UserFactory(email='user_net@admin.com', name="Auser",
                                        user_connected=1)  # user_connected = Network
        self.application = ApplicationFactory()
        self.incidentTemplate = IncidentTemplateFactory(template_id=1)
        self.domain = DomainFactory(domain_id=1, domain='api-dev-us.medic52.com')
        self.domain = DomainFactory(domain='api-dev-au.medic52.com', is_active=True)
        self.domain = DomainFactory(domain='testserver', is_active=True)
        self.resort = ResortFactory(domain_id=self.domain)
        self.userRoles = UserRolesFactory(role_id=3, key='manager', order=3)
        self.network_user_resort_map = UserResortMapFactory(user=self.network_user, resort=self.resort, role_id=3)
        self.incidentStatus = IncidentStatusFactory(incident_status_id=1, key="New Status Test 1")

        self.c = APIClient()
        self.token = TokenFactory(user=self.network_user)

    def testGetIncidentStatus(self):
        """
        Purpose - Code coverage
        Ticket no - #332
        Date created - 08/03/2015
        Date updated - 08/03/2015
        Updates made:
         -
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentStatusTestCase.testGetIncidentStatus
        """
        from django.db import connection

        with connection.cursor() as c:
            c.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        incident_json = {
            "name": "Gary Barlow",
            "email": "garry@barrlow.com",
            "phone": "+50672514236",
            "dob": "1978-07-15",
            "sex": "male",
            "address": "5th Avenue, San Diego",
            "suburb": "Los Ranchos",
            "state": "California",
            "country": "United States",
            "postcode": "12152"
        }

        response = self.c.post('/api/v3/incidents/',
                               incident_json, format='json')

        self.assertEqual(response.status_code, 200)
        incident_id = json.loads(response.content)['incident_id']
        response = self.c.get('/api/v3/incidents/%s/status/' % incident_id,
                              {}, format='json')
        self.assertEqual(response.status_code, 200)


class IncidentNotesTestCase(APITestCase):
    def setUp(self):
        self.network_user = UserFactory(email='user_net@admin.com', name="Auser",
                                        user_connected=1)  # user_connected = Network
        self.application = ApplicationFactory()
        self.incidentTemplate = IncidentTemplateFactory(template_id=1)
        self.domain = DomainFactory(domain_id=1, domain='api-dev-us.medic52.com')
        self.domain = DomainFactory(domain='api-dev-au.medic52.com', is_active=True)
        self.domain = DomainFactory(domain='testserver', is_active=True)
        self.resort = ResortFactory(domain_id=self.domain)
        self.userRoles = UserRolesFactory(role_id=3, key='manager', order=3)
        self.network_user_resort_map = UserResortMapFactory(user=self.network_user, resort=self.resort, role_id=3)
        self.incidentStatus = IncidentStatusFactory(incident_status_id=1, key="New Status Test 1")

        self.c = APIClient()
        self.token = TokenFactory(user=self.network_user)

    def testIncidentNotes(self):
        """
        Purpose - Code coverage
        Ticket no - #332
        Date created - 08/04/2015
        Date updated - 08/04/2015
        Updates made:
         -
        Additional comment:
         -
        command:
         - python manage.py test apps.incidents.tests.IncidentNotesTestCase.testIncidentNotes
        """
        from django.db import connection

        with connection.cursor() as c:
            c.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.network_user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        incident_json = {
            "name": "Gary Barlow",
            "email": "garry@barrlow.com",
            "phone": "+50672514236",
            "dob": "1978-07-15",
            "sex": "male",
            "address": "5th Avenue, San Diego",
            "suburb": "Los Ranchos",
            "state": "California",
            "country": "United States",
            "postcode": "12152"
        }

        response = self.c.post('/api/v3/incidents/',
                               incident_json, format='json')

        self.assertEqual(response.status_code, 200)
        incident_id = json.loads(response.content)['incident_id']
        response = self.c.post('/api/v3/incidents/%s/notes/' % incident_id,
                               {"field_52ca448dg94ja3": "Ambulance arrives at LA hospital",
                                "field_52ca448dg94ja4": "2015-06-11 08:58:27"}, format='json')
        self.assertEqual(response.status_code, 200)
        response = self.c.post('/api/v3/incidents/%s/notes/' % incident_id,
                               {"field_52ca448dg94ja3": "Patient is in the hospital",
                                "field_52ca448dg94ja4": "2015-06-11 08:59:27"}, format='json')
        self.assertEqual(response.status_code, 200)
        response = self.c.get('/api/v3/incidents/%s/notes/' % incident_id,
                              {}, format='json')
        self.assertEqual(response.status_code, 200)
