import datetime
import json
from datetime import date

from django.conf import settings
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient

from apps.authentication.factory.oauth_factory import ApplicationFactory, TokenFactory
from apps.custom_user.factory.user_factory import UserFactory, UserRolesFactory
from apps.incidents.factory.incident_factory import IncidentFactory
from apps.incidents.factory.incident_factory import IncidentStatusFactory
from apps.resorts.factory.resort_factory import IncidentTemplateFactory, ResortFactory, UserResortMapFactory
from apps.routing.factory.routing_factory import DomainFactory


class ReportsTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user_other = UserFactory(email='user_other@noowner.com', name="Other", user_connected=1)  # Network user
        self.user2 = UserFactory(email='user2network@admin.com', name="User_network", user_connected=1)  # Network user
        self.user_solo = UserFactory(email='user_solo_3321@admin.com', name="User_solo", user_connected=0)  # SOLO user
        self.application = ApplicationFactory()
        self.incidentTemplate = IncidentTemplateFactory(template_id=1)
        self.domain = DomainFactory(domain_id=1)
        self.domain = DomainFactory(domain='api-dev-au.medic52.com', is_active=True)
        # self.domain = DomainFactory(domain='testserver', is_active=True)
        self.resort = ResortFactory(domain_id=self.domain)
        self.userRoles = UserRolesFactory(role_id=3, key='manager', order=3)
        self.user_resort_map = UserResortMapFactory(user=self.user2, resort=self.resort, role_id=3)
        self.user_resort_map1 = UserResortMapFactory(user=self.user_solo, resort=self.resort, role_id=3)
        self.user_resort_map2 = UserResortMapFactory(user=self.user_other, resort=self.resort, role_id=3)
        self.incidentStatus = IncidentStatusFactory(incident_status_id=1)
        self.incidentStatus2 = IncidentStatusFactory(incident_status_id=2, key="status2")
        self.c = APIClient()
        self.token = TokenFactory(user=self.user2)

        # TODO: add report factory to use in Update report test.
        self.report = None

    def testMobileBarReport(self):
        """
        Purpose - Test for Bar chart API
        Ticket no - #298
        Date created - 07/27/2015
        Date updated - 07/27/2015
        Updates made:
         - Test for Bar chart API
        Additional comment:
         - NOT COMPLETED YET.
        command:
         - python manage.py test apps.incidents.tests.ReportsTestCase.testMobileBarReport
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
        response = self.c.post('/api/v3/auth/login/', {'email': self.user2.email, 'password': '1234'}, format='json')

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

        for i in range(0, 6):
            response = self.c.post('/api/v3/incidents/',
                                   incident_json, format='json')
            # print response
            self.assertEqual(response.status_code, 200)

        payload = [
            {
                "date": {
                    "datefrom": date.today().strftime("%Y-%m-%d 00:00:01"),
                    "dateto": date.today().strftime("%Y-%m-%d 23:59:59")
                },
                "data": {
                    "total_incident": []
                }
            },
            {
                "date": {
                    "datefrom": date.today().strftime("%Y-%m-%d 00:00:01"),
                    "dateto": date.today().strftime("%Y-%m-%d 23:59:59")
                },
                "data": {
                    "sex": [
                        "male"
                    ]
                }
            }
        ]
        # Filter by date range
        response = self.c.post('/api/v3/reports/bar/',
                               payload, format='json')
        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.content)
        self.assertIsNotNone(json_response[0][0]['date'], "date is none")
        self.assertIsNotNone(json_response[0][0]['field'], "field is none")
        self.assertIsNotNone(json_response[0][0]['count'], "count is none")
        self.assertEqual(json_response[0][0]['count'], 6)
        self.assertIsNotNone(json_response[0][1]['date'], "date is none")
        self.assertIsNotNone(json_response[0][1]['field'], "field is none")
        self.assertIsNotNone(json_response[0][1]['count'], "count is none")
        self.assertEqual(json_response[0][1]['count'], 6)

    def testTableReport(self):
        """
        Purpose - Test for Table report API
        Ticket no - #299
        Date created - 07/07/2015
        Date updated - 08/30/2015
        Updates made:
         - Test for Table report API
         - Update to new input and output data format.
        Additional comment:
         - Test for Table report API
        command:
         - python manage.py test apps.incidents.tests.ReportsTestCase.testTableReport
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
        response = self.c.post('/api/v3/auth/login/', {'email': self.user2.email, 'password': '1234'}, format='json')

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
            "postcode": "12152",
            "field_52d47a654d1cc": 2,
            "field_52d47a654d1dd": "garry@barrlow.com",
            "field_52d47a654d1ee": "1978-07-15",
            "field_52d47a654d1ff": "male",
            "field_52d47a654d1bb": "Gary Barlow",
            "field_52d47a654d1cc": 2,
            "field_52d47a654d1dd": "garry@barrlow.com",
            "field_52d47a654d1ee": "1978-07-15",
            "field_52d47a654d1ff": "male",
            "field_52ca445d62ba6": "Good",
            "field_52dd8c049b005": 50,
            "field_52ca445d62ba1": "23",
            "field_52ca456962ba8": {
                "lat": "-37.718244",
                "long": "144.96191799999997"
            },
            "occupation": "Software Developer",
            "notes": [
                {
                    "note_id": 234,
                    "note_by": str(self.user2.user_id),
                    "note_date": date.today().strftime("%Y-%m-%d %H:%M:%S"),
                    "note": "Holla Holla"
                }
            ]
        }

        for i in range(0, 3):
            response = self.c.post('/api/v3/incidents/',
                                   incident_json, format='json')
            self.assertEqual(response.status_code, 200)
            incident_id = json.loads(response.content)['incident_id']
            response = self.c.get('/api/v3/incidents/%s/' % str(incident_id),
                                  {}, format='json')
            self.assertEqual(response.status_code, 200)
            note = {
                "field_52ca448dg94ja4": "2015-02-15 21:45:03",
                "field_52ca448dg94ja3": "Holla Holla"
            }
            response = self.c.post('/api/v3/incidents/%s/notes/' % str(incident_id),
                                   note, format='json')
            self.assertEqual(response.status_code, 200)

        for i in range(0, 3):
            incident_json['name'] = "Britney Spears"
            response = self.c.post('/api/v3/incidents/',
                                   incident_json, format='json')
            self.assertEqual(response.status_code, 200)
            incident_id = json.loads(response.content)['incident_id']
            note = {
                "field_52ca448dg94ja4": "2015-02-15 21:45:03",
                "field_52ca448dg94ja3": "Holla Holla"
            }
            response = self.c.post('/api/v3/incidents/%s/notes/' % str(incident_id),
                                   note, format='json')
            self.assertEqual(response.status_code, 200)

        # Filter by date range
        response = self.c.post('/api/v3/reports/table/?datefrom=%s&dateto=%s&chunk=%s&offset=%s&format=json' % (
            date.today().strftime("%Y-%m-%d 00:00:01"), date.today().strftime("%Y-%m-%d 23:59:59"), '4', '0'),
                               {
                                   "name": ["Gary Barlow", "Britney Spears"],
                                   "occupation": ['Software Developer', 'Painter'],
                                   "notes____field_52ca448dg94ja3": ["Holla Holla"],
                                   "field_52ca456962ba8____lat": ["-37.718244", "40.0000"],
                                   "field_52ca456962ba8____long": ["144.96191799999997"],
                                   "field_52ca445d62ba6": ["Good"],
                                   "field_52dd8c049b005": [50],
                                   # "field_52ca445d62ba1": ["23"]
                               }, format='json')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response['count'], 6)
        self.assertEqual(json_response['chunk'], 4)
        self.assertEqual(json_response['offset'], 0)

        results = json_response.get('results', None)
        self.assertTrue(results != None, "Results is empty")

        result_0 = results[0]

        # Check for data
        self.assertEqual(result_0['patient']['name'], "Britney Spears")

    def testMobileReportList(self):
        """
        Purpose - Test for CRUD Reporting API
        Ticket no - #300
        Date created - 07/07/2015
        Date updated - 08/28/2015
        Updates made:
         - Test for CRUD Reporting API
        Additional comment:
         - Test for CRUD Reporting API
        command:
         - python manage.py test apps.incidents.tests.ReportsTestCase.testMobileReportList
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
        response = self.c.post('/api/v3/auth/login/', {'email': self.user2.email, 'password': '1234'}, format='json')

        create_data = {
            "label": "some label",
            "global": 1,
            "type": "bar",
            "config": {
                "url": {
                    "datefrom": date.today().strftime("%Y-%m-%d 00:00:01"),
                    "dateto": date.today().strftime("%Y-%m-%d 11:59:59"),
                    "daterange": "-7d",
                    "group_by": "field_52ca430462b9a",
                    "group_by_2": "field_54b084fb2d255",
                    "compare_with": "field_52ca3fcc59d29",
                    "datecomparefrom": date.today().strftime("%Y-%m-%d 00:00:01"),
                    "datecompareto": date.today().strftime("%Y-%m-%d 11:59:59"),
                    "datecomparerange": "-7d",
                    "display": "field_52d47a654d1fc",
                    "compare_to": "field_52ca3fcc59d29",
                    "show_count": 5
                },
                "body": {
                    "name": ["Krish", "Shaun"],
                    "occupation": ["Software Developer", "Painter"],
                    "notes____field_52ca448dg94ja3": ["new note"],
                    "field_52ca456962ba8____lat": ["-37.718244", "40.0000"],
                    "field_52ca456962ba8____long": ["144.96191799999997"],
                    "field_52ca445d62ba6": ["Good"],
                    "field_52dd8c049b005": [50],
                    "field_52ca445d62ba1": ["23"],
                    "field_52d4798f6d227____preexisting_injury": ["817", "820"]
                }
            }
        }

        # 5 Global reports
        for label in ["report 1", "report 2", "report 3", "report 4", "report 5"]:
            create_data['label'] = label
            response = self.c.post('/api/v3/reports/',
                                   create_data, format='json')
            self.assertEqual(response.status_code, 200)

        # 5 NONE Global reports
        for label in ["report 6", "report 7", "report 8", "report 9", "report 10"]:
            create_data['label'] = label
            create_data['global'] = 0
            response = self.c.post('/api/v3/reports/',
                                   create_data, format='json')
            self.assertEqual(response.status_code, 200)

        # Try report list with logged in user who created them.
        response = self.c.get('/api/v3/reports/',
                              {}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['count'], 10)
        self.assertIsNotNone(json.loads(response.content)['results'], "Results is none")

        # Try report list with a DIFFERENT logged in user than created by.
        response = self.c.post('/api/v3/auth/login/', {'email': self.user_other.email, 'password': '1234'},
                               format='json')
        response = self.c.get('/api/v3/reports/',
                              {}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['count'], 5)  # Only the global reports should be returned
        self.assertIsNotNone(json.loads(response.content)['results'], "Results is none")
        for report in json.loads(response.content)['results']:
            self.assertEqual(report['global'], 1)  # each report should be global

        # Try report list with a SOLO logged in user.
        response = self.c.post('/api/v3/auth/login/', {'email': self.user_solo.email, 'password': '1234'},
                               format='json')
        response = self.c.get('/api/v3/reports/',
                              {}, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.content)['detail'], 'you do not have permission to list report')

    def testMobileReportCreate(self):
        """
        Purpose - Test for CRUD Reporting API
        Ticket no - #300
        Date created - 07/07/2015
        Date updated - 08/28/2015
        Updates made:
         - Test for CRUD Reporting API
        Additional comment:
         - Test for CRUD Reporting API
        command:
         - python manage.py test apps.incidents.tests.ReportsTestCase.testMobileReportCreate
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
        response = self.c.post('/api/v3/auth/login/', {'email': self.user2.email, 'password': '1234'}, format='json')
        create_data = {
            "label": "Incidents by location",
            "global": 1,
            "type": "bar",
            "config": {
                "url": {
                    "datefrom": date.today().strftime("%Y-%m-%d 00:00:01"),
                    "dateto": date.today().strftime("%Y-%m-%d 11:59:59"),
                    "daterange": "-7d",
                    "group_by": "field_52ca430462b9a",
                    "group_by_2": "field_54b084fb2d255",
                    "compare_with": "field_52ca3fcc59d29",
                    "datecomparefrom": date.today().strftime("%Y-%m-%d 00:00:01"),
                    "datecompareto": date.today().strftime("%Y-%m-%d 11:59:59"),
                    "datecomparerange": "-7d",
                    "display": "field_52d47a654d1fc",
                    "compare_to": "field_52ca3fcc59d29",
                    "show_count": 5
                },
                "body": {
                    "name": ["Krish", "Shaun"],
                    "occupation": ["Software Developer", "Painter"],
                    "notes____field_52ca448dg94ja3": ["new note"],
                    "field_52ca456962ba8____lat": ["-37.718244", "40.0000"],
                    "field_52ca456962ba8____long": ["144.96191799999997"],
                    "field_52ca445d62ba6": ["Good"],
                    "field_52dd8c049b005": [50],
                    "field_52ca445d62ba1": ["23"],
                    "field_52d4798f6d227____preexisting_injury": ["817", "820"]
                }
            }
        }
        response = self.c.post('/api/v3/reports/',
                               create_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(json.loads(response.content)['report_id'], "report id is None")
        self.assertIsNotNone(json.loads(response.content)['config'], "config is None")
        self.assertEqual(json.loads(response.content)['type'], "bar")
        self.assertEqual(json.loads(response.content)['global'], 1)
        self.assertEqual(json.loads(response.content)['label'], "Incidents by location")

        response = self.c.post('/api/v3/auth/login/', {'email': self.user_solo.email, 'password': '1234'},
                               format='json')
        response = self.c.post('/api/v3/reports/',
                               create_data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.content)['detail'], "you do not have permission to create report")

    def testMobileReportUpdate(self):
        """
        Purpose - Test for CRUD Reporting API
        Ticket no - #300
        Date created - 07/07/2015
        Date updated - 08/28/2015
        Updates made:
         - Test for CRUD Reporting API
         - Adjust to data format and validate update is done.
        Additional comment:
         - Test for CRUD Reporting API
        command:
         - python manage.py test apps.incidents.tests.ReportsTestCase.testMobileReportUpdate
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
        response = self.c.post('/api/v3/auth/login/', {'email': self.user2.email, 'password': '1234'}, format='json')

        response = self.c.post('/api/v3/reports/',
                               {
                                   "label": "Incidents by location",
                                   "global": 0,
                                   "type": "bar",
                                   "config": {
                                       "url": {
                                           "datefrom": date.today().strftime("%Y-%m-%d 00:00:01"),
                                           "dateto": date.today().strftime("%Y-%m-%d 11:59:59"),
                                           "daterange": "-7d",
                                           "group_by": "field_52ca430462b9a",
                                           "group_by_2": "field_54b084fb2d255",
                                           "compare_with": "field_52ca3fcc59d29",
                                           "datecomparefrom": date.today().strftime("%Y-%m-%d 00:00:01"),
                                           "datecompareto": date.today().strftime("%Y-%m-%d 11:59:59"),
                                           "datecomparerange": "-7d",
                                           "display": "field_52d47a654d1fc",
                                           "compare_to": "field_52ca3fcc59d29",
                                           "show_count": 5
                                       },
                                       "body": {
                                           "name": ["Krish", "Shaun"],
                                           "occupation": ["Software Developer", "Painter"],
                                           "notes____field_52ca448dg94ja3": ["new note"],
                                           "field_52ca456962ba8____lat": ["-37.718244", "40.0000"],
                                           "field_52ca456962ba8____long": ["144.96191799999997"],
                                           "field_52ca445d62ba6": ["Good"],
                                           "field_52dd8c049b005": [50],
                                           "field_52ca445d62ba1": ["23"],
                                           "field_52d4798f6d227____preexisting_injury": ["817", "820"]
                                       }
                                   }
                               }, format='json')
        self.assertEqual(response.status_code, 200)
        created_report_id = json.loads(response.content)['report_id']

        update_data = {
            "label": "Incidents by location111",
            "global": 1,
            "type": "table",
            "config": {
                "url": {
                    "datefrom": "2015-05-22 07:38:15",
                    "dateto": "2015-05-23 07:38:15",
                    "daterange": "-14d",
                    "group_by": "field_52ca430462b9a",
                    "group_by_2": "field_54b084fb2d255",
                    "compare_with": "field_52ca3fcc59d29",
                    "datecomparefrom": "2015-04-21 07:38:15",
                    "datecompareto": "2015-04-22 07:38:15",
                    "datecomparerange": "-7d",
                    "display": "field_52d47a654d1fc",
                    "compare_to": "field_52ca3fcc59d29",
                    "show_count": 5
                },
                "body": {
                    "name": ["Krish", "Shaun"],
                    "occupation": ["Software Developer", "Painter"],
                    "notes____field_52ca448dg94ja3": ["new note"],
                    "field_52ca456962ba8____lat": ["-37.718244", "40.0000"],
                    "field_52ca456962ba8____long": ["144.96191799999997"],
                    "field_52ca445d62ba6": ["Good"],
                    "field_52dd8c049b005": [50],
                    "field_52ca445d62ba1": ["23"],
                    "field_52d4798f6d227____preexisting_injury": ["817", "820"]
                }
            }
        }

        response = self.c.put('/api/v3/reports/%s/' % created_report_id,
                              update_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['label'], "Incidents by location111",
                         "Returned data doesn't match with sent to update")
        self.assertIsNotNone(json.loads(response.content)['config'], "config is None")
        self.assertEqual(json.loads(response.content)['type'], "table")
        self.assertEqual(json.loads(response.content)['global'], 1)
        self.assertEqual(json.loads(response.content)['config']['url']['datefrom'], "2015-05-22 07:38:15")
        self.assertEqual(json.loads(response.content)['config']['url']['dateto'], "2015-05-23 07:38:15")
        self.assertEqual(json.loads(response.content)['config']['url']['daterange'], "-14d")

        response = self.c.post('/api/v3/auth/login/', {'email': self.user_solo.email, 'password': '1234'},
                               format='json')
        response = self.c.put('/api/v3/reports/%s/' % created_report_id,
                              update_data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.content)['detail'], "you do not have permission to update report")

    def testMobileReportGet(self):
        """
        Purpose - Test for CRUD Reporting API
        Ticket no - #300
        Date created - 07/07/2015
        Date updated - 08/28/2015
        Updates made:
         - Test for CRUD Reporting API
        Additional comment:
         - Test for CRUD Reporting API
        command:
         - python manage.py test apps.incidents.tests.ReportsTestCase.testMobileReportGet
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
        response = self.c.post('/api/v3/auth/login/', {'email': self.user2.email, 'password': '1234'}, format='json')

        config = {
            "url": {
                "datefrom": date.today().strftime("%Y-%m-%d 00:00:01"),
                "dateto": date.today().strftime("%Y-%m-%d 11:59:59"),
                "daterange": "-7d",
                "group_by": "field_52ca430462b9a",
                "group_by_2": "field_54b084fb2d255",
                "compare_with": "field_52ca3fcc59d29",
                "datecomparefrom": date.today().strftime("%Y-%m-%d 00:00:01"),
                "datecompareto": date.today().strftime("%Y-%m-%d 11:59:59"),
                "datecomparerange": "-7d",
                "display": "field_52d47a654d1fc",
                "compare_to": "field_52ca3fcc59d29",
                "show_count": 5
            },
            "body": {
                "name": ["Krish", "Shaun"],
                "occupation": ["Software Developer", "Painter"],
                "notes____field_52ca448dg94ja3": ["new note"],
                "field_52ca456962ba8____lat": ["-37.718244", "40.0000"],
                "field_52ca456962ba8____long": ["144.96191799999997"],
                "field_52ca445d62ba6": ["Good"],
                "field_52dd8c049b005": [50],
                "field_52ca445d62ba1": ["23"],
                "field_52d4798f6d227____preexisting_injury": ["817", "820"]
            }
        }
        response = self.c.post('/api/v3/reports/',
                               {
                                   "label": "Incidents by location",
                                   "global": 1,
                                   "type": "bar",
                                   "config": config
                               }, format='json')
        self.assertEqual(response.status_code, 200)
        created_report_id = json.loads(response.content)['report_id']
        response = self.c.get('/api/v3/reports/%s/' % created_report_id,
                              {}, format='json')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(json_response['label'], "Incidents by location")
        self.assertEqual(json_response['type'], "bar")
        self.assertEqual(json_response['report_id'], created_report_id)
        self.assertEqual(json_response['global'], 1)
        self.assertEqual(json_response['config'], config)

        response = self.c.post('/api/v3/auth/login/', {'email': self.user_solo.email, 'password': '1234'},
                               format='json')
        response = self.c.get('/api/v3/reports/%s/' % created_report_id,
                              {}, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.content)['detail'], "you do not have permission to retrieve report")

    def testReportPatrollersList(self):
        """
        Purpose - Test for Patrollers Report API
        Ticket no - #540
        Date created - 09/17/2016
        Date updated - 09/17/2016
        Updates made:
         - No one yet.
        Additional comment:
        command:
         - python manage.py test apps.reports.tests.ReportsTestCase.testReportPatrollersList
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
        response = self.c.post('/api/v3/auth/login/', {'email': self.user2.email, 'password': '1234'}, format='json')


        payload = {
            "datefrom": date.today().strftime("%Y-%m-%d 00:00:01"),
            "dateto": date.today().strftime("%Y-%m-%d 23:59:59"),
            "output_format": "json",
            "ofsset": 2,
            "chunk": 10,
            "order_by": "name",
            "order_by_direction": "desc"
        }
        # Filter by date range
        response = self.c.get('/api/v3/reports/patrollers/', payload, format='json')
        self.assertEqual(response.status_code, 200)
        #
        json_response = json.loads(response.content)
        self.assertTrue(json_response['success'], "unsuccessful")
        self.assertGreaterEqual(json_response['total_rows'], 0)
        self.assertIsNotNone(json_response['data'], "count is none")

        #Iterate results


    def testReportCaseStatusList(self):
        """
        Purpose - Test for Case Status Report API
        Ticket no - #541
        Date created - 09/17/2016
        Date updated - 09/17/2016
        Updates made:
         - No one yet.
        Additional comment:
        command:
         - python manage.py test apps.reports.tests.ReportsTestCase.testReportCaseStatusList
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
        response = self.c.post('/api/v3/auth/login/', {'email': self.user2.email, 'password': '1234'}, format='json')

        payload = {
            "datefrom": date.today().strftime("%Y-%m-%d 00:00:00"),
            "dateto": date.today().strftime("%Y-%m-%d 23:59:59"),
            "output_format": "json",
            "ofsset": 2,
            "chunk": 10,
            "status": "1,2,3,4,5,6,7,8"
        }
        # Filter by date range
        response = self.c.get('/api/v3/reports/status/', payload, format='json')
        self.assertEqual(response.status_code, 200)
        #
        json_response = json.loads(response.content)
        self.assertGreaterEqual(json_response['chunk'], 0)
        self.assertGreaterEqual(json_response['offset'], 0)
        self.assertGreaterEqual(json_response['count'], 0)
        self.assertIsNotNone(json_response['results'], "count is none")
        self.assertIsNotNone(json_response['summary'], "summary is none")

        # Iterate results

class ReportsTestCase2(APITestCase):
    def setUp(self):
        self.incident_json = IncidentsTestCase2.incident_json.copy()
        self.user = UserFactory(user_connected=1, is_active=True)
        self.userPatroller = UserFactory(email='patroller@yahoo.com', name='Mr Patroller',
                                         user_connected=1, is_active=True)
        self.userPatrollerSolo = UserFactory(email='patrollersolo@yahoo.com', name='Mr Patroller Solo',
                                             user_connected=0, is_active=True)
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
                                                           user=self.userPatroller, resort=self.resort)
        self.userResortMapPatrollerSolo = UserResortMapFactory(role_id=self.userRolePatroller.role_id,
                                                               user=self.userPatrollerSolo, resort=self.resort)
        self.userResortMapDispatcher = UserResortMapFactory(role_id=self.userRoleDispatcher.role_id,
                                                            user=self.userDispatcher, resort=self.resort)
        self.userResortMapManager = UserResortMapFactory(role_id=self.userRoleManager.role_id,
                                                         user=self.user, resort=self.resort)
        # create and set incident status
        self.incidentStatus = IncidentsTestCase2.createIncidentStatus()
        self.incident = IncidentFactory(resort=self.resort, assigned_to=self.user,
                                        incident_status=self.incidentStatus[1])
        self.c = APIClient()
        self.token = TokenFactory(user=self.user)

        from django.db import connection

        with connection.cursor() as c:
            c.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')

    def testPieChartReport(self):
        """
        Purpose - Test for Report Pie chart API
        Ticket no - #296
        Date created - 07/16/2015
        Date updated - 08/28/2015
        Updates made:
         - Test for Report Pie chart API
         - Updates to check for actual data in response not only status code
         - Use the updated doc on apiary and updated postman to update the test according to updated input and output
        Additional comment:
         - Test for Report Pie chart API
        command:
         - python manage.py test apps.incidents.tests.ReportsTestCase2.testPieChartReport
        """
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')

        incident_json_data = self.incident_json.copy()
        date_start = timezone.now()
        # create 1st incident
        incident_json_data["field_52d4798f6d227"] = [
            {
                "preexisting_injury": "817",
                "body_part": "130",  # shoulder
                "injury_location": "152",
                "injury_type": "158"
            }
        ]
        response = self.c.post('/api/v3/incidents/', data=json.dumps(incident_json_data),
                               content_type='application/json')
        # create 2nd incident
        incident_json_data["field_52d4798f6d227"] = [
            {
                "preexisting_injury": "817",
                "body_part": "140",  # knee
                "injury_location": "152",
                "injury_type": "158"
            }
        ]
        response = self.c.post('/api/v3/incidents/', data=json.dumps(incident_json_data),
                               content_type='application/json')

        # create 3rd incident
        incident_json_data["field_52d4798f6d227"] = [
            {
                "preexisting_injury": "817",
                "body_part": "",  # unknown
                "injury_location": "152",
                "injury_type": "158"
            }
        ]
        response = self.c.post('/api/v3/incidents/', data=json.dumps(incident_json_data),
                               content_type='application/json')

        date_end = timezone.now()

        dt_from = (date_start - timezone.timedelta(days=1)).strftime('%Y-%m-%d 00:00:00')
        dt_to = (date_end + timezone.timedelta(days=1)).strftime('%Y-%m-%d 00:00:00')

        # test for report pie chart API
        body = [
            {
                "date": {
                    "datefrom": dt_from,
                    "dateto": dt_to
                },
                "data": {
                    "field_52d4798f6d227____body_part": []
                }
            }
        ]
        response = self.c.post('/api/v3/reports/pie/', data=body, format='json')
        data = response.data
        for report in data:
            if report['name'] == 'shoulder':
                self.assertEqual(report['count'], 1, "1 incident for shoulder injury")
            elif report['name'] == 'knee':
                self.assertEqual(report['count'], 1, "1 incident for knee injury")
            elif report['name'] == 'Unknown':
                self.assertEqual(report['count'], 2, "2 incident for unknown")

    def testTimelineReport(self):
        """
        Purpose - Test Timeline Report API
        Ticket no - #297
        Date created - 07/17/2015
        Date updated - 08/28/2015
        Updates made:
         - Test Timeline Report API
         - Updates to check for the actual output from the API call rather than just the status code
         - Use the updated doc on apiary and updated postman to update the test according to updated input and output
        Additional comment:
         - Test Timeline Report API
        command:
         - python manage.py test apps.incidents.tests.ReportsTestCase2.testTimelineReport
        """
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')

        incident_json_data = self.incident_json.copy()
        date_start = datetime.datetime.today()

        # create 1st batch of incidents current date minus - 3 days
        dateBefore3days = date_start - timedelta(days=3)

        # shoulder incident
        incident_json_data["field_52d4798f6d227"] = [
            {
                "preexisting_injury": "817",
                "body_part": "130",  # shoulder
                "injury_location": "152",
                "injury_type": "158"
            }
        ]
        response = self.c.post('/api/v3/incidents/', data=json.dumps(incident_json_data),
                               content_type='application/json')
        incident_id = response.data['incident_id']
        update_incident_json = {"dt_created": dateBefore3days.strftime('%Y-%m-%d %H:%M:%S')}
        response = self.c.put('/api/v3/incidents/%s/' % str(incident_id),
                              update_incident_json, format='json')
        # knee incident
        incident_json_data["field_52d4798f6d227"] = [
            {
                "preexisting_injury": "817",
                "body_part": "140",  # knee
                "injury_location": "152",
                "injury_type": "158"
            }
        ]
        response = self.c.post('/api/v3/incidents/', data=json.dumps(incident_json_data),
                               content_type='application/json')
        incident_id = response.data['incident_id']

        update_incident_json = {"dt_created": dateBefore3days.strftime('%Y-%m-%d %H:%M:%S')}
        response = self.c.put('/api/v3/incidents/%s/' % str(incident_id),
                              update_incident_json, format='json')

        # create 2nd batch of incidents current date minus - 2 days
        dateBefore2days = date_start - timedelta(days=2)

        # shoulder incident
        incident_json_data["field_52d4798f6d227"] = [
            {
                "preexisting_injury": "817",
                "body_part": "130",  # shoulder
                "injury_location": "152",
                "injury_type": "158"
            }
        ]
        response = self.c.post('/api/v3/incidents/', data=json.dumps(incident_json_data),
                               content_type='application/json')
        incident_id = response.data['incident_id']
        update_incident_json = {"dt_created": dateBefore2days.strftime('%Y-%m-%d %H:%M:%S')}
        response = self.c.put('/api/v3/incidents/%s/' % str(incident_id),
                              update_incident_json, format='json')
        # knee incident
        incident_json_data["field_52d4798f6d227"] = [
            {
                "preexisting_injury": "817",
                "body_part": "140",  # knee
                "injury_location": "152",
                "injury_type": "158"
            }
        ]
        response = self.c.post('/api/v3/incidents/', data=json.dumps(incident_json_data),
                               content_type='application/json')
        incident_id = response.data['incident_id']
        update_incident_json = {"dt_created": dateBefore2days.strftime('%Y-%m-%d %H:%M:%S')}
        response = self.c.put('/api/v3/incidents/%s/' % str(incident_id),
                              update_incident_json, format='json')

        date_end = datetime.datetime.today() + timedelta(days=1)

        dt_from = (dateBefore3days - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
        dt_to = date_end.strftime('%Y-%m-%d %H:%M:%S')

        # test for report timeline API
        body = [
            {
                "date": {
                    "datefrom": dt_from,
                    "dateto": dt_to
                },
                "data": {
                    "field_52d4798f6d227____body_part": ["130"]
                }
            },
            {
                "date": {
                    "datefrom": dt_from,
                    "dateto": dt_to
                },
                "data": {
                    "field_52d4798f6d227____body_part": ["140"]
                }
            }
        ]
        response = self.c.post('/api/v3/reports/timeline/', data=body, format='json')

        data = response.data
        for report in data:
            for field in report:
                if isinstance(field['date'], datetime.date):
                    if field['date'].strftime('%Y-%m-%d') == dateBefore3days.strftime('%Y-%m-%d'):
                        if field['field'] == 1:
                            self.assertEqual(field['count'], 1, "1 shoulder incident of 3 days before current day")
                        elif field['field'] == 2:
                            self.assertEqual(field['count'], 1, "1 knee incident of 3 days before current day")
                    if field['date'].strftime('%Y-%m-%d') == dateBefore2days.strftime('%Y-%m-%d'):
                        if field['field'] == 1:
                            self.assertEqual(field['count'], 1, "1 shoulder incident of 2 days before current day")
                        elif field['field'] == 1:
                            self.assertEqual(field['count'], 1, "1 knee incident of 2 days before current day")

    def testNetworkUserReport(self):
        """
        Purpose - Test reports API - dont show user_connected = solo incidents
        Ticket no - #307
        Date created - 07/18/2015
        Date updated - 07/29/2015
        Updates made:
         - Test reports API - dont show user_connected = solo incidents
         - If Solo User creates incident then it should not be part of the report
         - Filtering parameter that is being passed as json in the body of the report table API
        Additional comment:
         - Test reports API - dont show user_connected = solo incidents
        command:
         - python manage.py test apps.incidents.tests.ReportsTestCase2.testNetworkUserReport
        """
        response = self.client.post('/oauth/access_token/', {'grant_type': 'client_credentials',
                                                             'client_id': self.application.client_id,
                                                             'client_secret': self.application.client_secret})
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/',
                               {'email': self.userPatrollerSolo.email, 'password': '1234'}, format='json')

        incident_json_data = self.incident_json.copy()

        date_start = datetime.datetime.today() - timedelta(days=7)
        # create 1st incident
        response = self.c.post('/api/v3/incidents/', data=json.dumps(incident_json_data),
                               content_type='application/json')
        # create 2nd incident
        response = self.c.post('/api/v3/incidents/', data=json.dumps(incident_json_data),
                               content_type='application/json')
        date_end = datetime.datetime.today() + timedelta(days=7)

        # Ensure these APIs dont show stats incidents from solo users
        dt_from = date_start.strftime('%Y-%m-%d %H:%M:%S')
        dt_to = date_end.strftime('%Y-%m-%d %H:%M:%S')
        chunk = 100
        offset = 0
        body = {
            "field_52ca430462b9a": "yes",
            "field_52dd8a57e95a7": "POC",
            "field_52dd8a57e95a7": "Giro",
            "field_54b084fb2d255": "no",
            "field_52ca3fcc59d29": "no"
        }

        response = self.c.post('/api/v3/auth/login/', {'email': self.userDispatcher.email, 'password': '1234'},
                               format='json')
        response = self.c.post('/api/v3/reports/table/?datefrom=%s&dateto=%s&chunk=%s&offset=%s&format=json' % (
            dt_from, dt_to, chunk, offset), body, format='json')

        # If Solo User creates incident then it should not be part of the report
        self.assertEqual(response.data['count'], 0)

        report_json = {
            "label": "Incidents by location",
            "global": 1,
            "type": "bar",
            "config": {
                "url": {
                    "dt_from": "yyyy-mm-dd",
                    "dt_to": "yyyy-mm-dd",
                    "dt_range": "-7d",
                    "group_by": "field_52ca430462b9a",
                    "group_by_2": "field_54b084fb2d255",
                    "compare_with": "field_52ca3fcc59d29",
                    "dt_compare_from": "yyyy-mm-dd",
                    "dt_compare_to": "yyyy-mm-dd",
                    "dt_compare_range": "-7d",
                    "display": "field_52d47a654d1fc",
                    "compare_to": "field_52ca3fcc59d29",
                    "show_count": 5
                },
                "body": {
                    "field_52ca430462b9a": "yes",
                    "field_52dd8a57e95a7": "POC",
                    "field_52dd8a57e95a7": "Giro",
                    "field_54b084fb2d255": "no",
                    "field_52ca3fcc59d29": "no",
                    "field_52d47a654d1fc": 4,
                    "field_52d47a654d1fd": 3
                }
            }
        }

        # Create report deny to solo user
        response = self.c.post('/api/v3/auth/login/',
                               {'email': self.userPatrollerSolo.email, 'password': '1234'}, format='json')
        response = self.c.post('/api/v3/reports/', data=json.dumps(report_json),
                               content_type='application/json')
        self.assertEqual(response.status_code, 403)

        report_id = ''
        if response.status_code == 200:
            report_id = str(response.data['report_id'])

        # List Reports
        response = self.c.get('/api/v3/reports/', {}, content_type='application/json')

        # Update Report deny to solo user
        response = self.c.put('/api/v3/reports/' + report_id + '/', data=json.dumps(report_json),
                              content_type='application/json')
        self.assertEqual(response.status_code, 403)

        # Get Report deny to solo user
        response = self.c.get('/api/v3/reports/' + report_id + '/', {}, content_type='application/json')
        self.assertEqual(response.status_code, 403)

        # To check that SOLO user should not able run reports
        dt_from = date_start.strftime('%Y-%m-%d %H:%M:%S')
        dt_to = date_end.strftime('%Y-%m-%d %H:%M:%S')
        chunk = 100
        offset = 0

        response = self.c.post('/api/v3/reports/table/?datefrom=%s&dateto=%s&chunk=%s&offset=%s&format=json' % (
            dt_from, dt_to, chunk, offset), body, format='json')
        self.assertEqual(response.status_code, 403)


class ChartScaleTest(APITestCase):
    def setUp(self):
        self.user = UserFactory(user_connected=1)
        self.application = ApplicationFactory(user=self.user)
        self.incidentTemplate = IncidentTemplateFactory(template_id=1)
        self.domain = DomainFactory(domain_id=1)
        self.domain = DomainFactory(domain='api-dev-au.medic52.com', is_active=True)
        self.domain = DomainFactory(domain='testserver', is_active=True)
        self.resort = ResortFactory(domain_id=self.domain, timezone='UTC')
        self.userRoles = UserRolesFactory(role_id=3, key='manager', order=3)
        self.user_resort_map = UserResortMapFactory(user=self.user, resort=self.resort, role_id=3)
        self.incidentStatus = IncidentStatusFactory(incident_status_id=1)
        self.incidentStatus2 = IncidentStatusFactory(incident_status_id=2, key="status2")

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

        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'},
                               format='json')
        self.assertEqual(response.status_code, 200)

        self.current_datetime = datetime.datetime.strptime("2014-01-01 10:00:00", "%Y-%m-%d %H:%M:%S")

    def testHourScale(self):
        try:
            # Create incidents on different hours of day
            for i in range(0, 3):
                for j in range(0, 2):
                    incident = IncidentFactory(resort=self.resort, assigned_to=self.user,
                                               incident_status=self.incidentStatus)
                    response = self.c.put('/api/v3/incidents/%s/' % incident.incident_id,
                                          {
                                              "field_52ca456962ba8": {
                                                  "lat": -27.059125784374054,
                                                  "long": 135,
                                                  "accuracy": 4
                                              },
                                              "dt_created": (
                                                  self.current_datetime + datetime.timedelta(hours=j, days=i)).strftime(
                                                  "%Y-%m-%d %H:%M:%S")
                                          }, format='json')

            response = self.c.post('/api/v3/reports/timeline/?resort_id=%s&date_from=%s' % (
                self.resort.resort_id, self.current_datetime.strftime("%Y-%m-%d 00:00:01")),
                                   [{"date": {"datefrom": "2014-01-01 00:00:01", "dateto": "2015-12-31 23:59:59"},
                                     "data": {"total_incident": []}, "scale": "hour"}], format='json')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.content)[9][0]['count'], 3)
            self.assertEqual(json.loads(response.content)[10][0]['count'], 3)
        except Exception as e:
            print e.message

    def testDayScale(self):
        try:
            self.current_datetime += datetime.timedelta(weeks=1)

            for i in range(0, 3):
                for j in range(0, 2):
                    incident = IncidentFactory(resort=self.resort, assigned_to=self.user,
                                               incident_status=self.incidentStatus)
                    response = self.c.put('/api/v3/incidents/%s/' % incident.incident_id,
                                          {
                                              "field_52ca456962ba8": {
                                                  "lat": -27.059125784374054,
                                                  "long": 135,
                                                  "accuracy": 4
                                              },
                                              "dt_created": (
                                                  self.current_datetime + datetime.timedelta(hours=j, days=i)).strftime(
                                                  "%Y-%m-%d %H:%M:%S")
                                          }, format='json')

            response = self.c.post('/api/v3/reports/timeline/?resort_id=%s&date_from=%s' % (
                self.resort.resort_id, self.current_datetime.strftime("%Y-%m-%d 00:00:01")),
                                   [{"date": {"datefrom": "2014-01-01 00:00:01", "dateto": "2015-12-31 23:59:59"},
                                     "data": {"total_incident": []}, "scale": "day"}], format='json')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.content)[7][0]['count'], 2)
            self.assertEqual(json.loads(response.content)[8][0]['count'], 2)
            self.assertEqual(json.loads(response.content)[9][0]['count'], 2)
        except Exception as e:
            print e.message

    def testDateScale(self):
        try:
            self.current_datetime += datetime.timedelta(weeks=1)

            for i in range(0, 3):
                for j in range(0, 2):
                    incident = IncidentFactory(resort=self.resort, assigned_to=self.user,
                                               incident_status=self.incidentStatus)
                    response = self.c.put('/api/v3/incidents/%s/' % incident.incident_id,
                                          {
                                              "field_52ca456962ba8": {
                                                  "lat": -27.059125784374054,
                                                  "long": 135,
                                                  "accuracy": 4
                                              },
                                              "dt_created": (
                                                  self.current_datetime + datetime.timedelta(hours=j, days=i)).strftime(
                                                  "%Y-%m-%d %H:%M:%S")
                                          }, format='json')

            response = self.c.post('/api/v3/reports/timeline/?resort_id=%s&date_from=%s' % (
                self.resort.resort_id, self.current_datetime.strftime("%Y-%m-%d 00:00:01")),
                                   [{"date": {"datefrom": "2014-01-01 00:00:01", "dateto": "2015-12-31 23:59:59"},
                                     "data": {"total_incident": []}, "scale": "date"}], format='json')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.content)[7][0]['count'], 2)
            self.assertEqual(json.loads(response.content)[8][0]['count'], 2)
            self.assertEqual(json.loads(response.content)[9][0]['count'], 2)
        except Exception as e:
            print e.message

    def testDayOfWeekScale(self):
        try:
            self.current_datetime += datetime.timedelta(weeks=1)

            for i in range(0, 3):
                for j in range(0, 2):
                    incident = IncidentFactory(resort=self.resort, assigned_to=self.user,
                                               incident_status=self.incidentStatus)
                    response = self.c.put('/api/v3/incidents/%s/' % incident.incident_id,
                                          {
                                              "field_52ca456962ba8": {
                                                  "lat": -27.059125784374054,
                                                  "long": 135,
                                                  "accuracy": 4
                                              },
                                              "dt_created": (
                                                  self.current_datetime + datetime.timedelta(hours=j, days=i)).strftime(
                                                  "%Y-%m-%d %H:%M:%S")
                                          }, format='json')

            response = self.c.post('/api/v3/reports/timeline/?resort_id=%s&date_from=%s' % (
                self.resort.resort_id, self.current_datetime.strftime("%Y-%m-%d 00:00:01")),
                                   [{"date": {"datefrom": "2014-01-01 00:00:01", "dateto": "2015-12-31 23:59:59"},
                                     "data": {"total_incident": []}, "scale": "day_of_week"}], format='json')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.content)[2][0]['count'], 2)
            self.assertEqual(json.loads(response.content)[3][0]['count'], 2)
            self.assertEqual(json.loads(response.content)[4][0]['count'], 2)
        except Exception as e:
            print e.message

    def testWeekOfYearScale(self):
        try:
            self.current_datetime += datetime.timedelta(weeks=1)

            for i in range(0, 3):
                for j in range(0, 2):
                    incident = IncidentFactory(resort=self.resort, assigned_to=self.user,
                                               incident_status=self.incidentStatus)
                    response = self.c.put('/api/v3/incidents/%s/' % incident.incident_id,
                                          {
                                              "field_52ca456962ba8": {
                                                  "lat": -27.059125784374054,
                                                  "long": 135,
                                                  "accuracy": 4
                                              },
                                              "dt_created": (
                                                  self.current_datetime + datetime.timedelta(days=j, weeks=i)).strftime(
                                                  "%Y-%m-%d %H:%M:%S")
                                          }, format='json')

            response = self.c.post('/api/v3/reports/timeline/?resort_id=%s&date_from=%s' % (
                self.resort.resort_id, self.current_datetime.strftime("%Y-%m-%d 00:00:01")),
                                   [{"date": {"datefrom": "2014-01-01 00:00:01", "dateto": "2015-12-31 23:59:59"},
                                     "data": {"total_incident": []}, "scale": "week_of_year"}], format='json')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.content)[1][0]['count'], 2)
            self.assertEqual(json.loads(response.content)[2][0]['count'], 2)
            self.assertEqual(json.loads(response.content)[3][0]['count'], 2)
        except Exception as e:
            print e.message

    def testMonthOfYearScale(self):
        try:
            self.current_datetime += datetime.timedelta(weeks=1)

            for i in range(0, 3):
                for j in range(0, 2):
                    incident = IncidentFactory(resort=self.resort, assigned_to=self.user,
                                               incident_status=self.incidentStatus)
                    response = self.c.put('/api/v3/incidents/%s/' % incident.incident_id,
                                          {
                                              "field_52ca456962ba8": {
                                                  "lat": -27.059125784374054,
                                                  "long": 135,
                                                  "accuracy": 4
                                              },
                                              "dt_created": (
                                                  self.current_datetime + datetime.timedelta(days=j,
                                                                                             weeks=i * 4)).strftime(
                                                  "%Y-%m-%d %H:%M:%S")
                                          }, format='json')

            response = self.c.post('/api/v3/reports/timeline/?resort_id=%s&date_from=%s' % (
                self.resort.resort_id, self.current_datetime.strftime("%Y-%m-%d 00:00:01")),
                                   [{"date": {"datefrom": "2014-01-01 00:00:01", "dateto": "2015-12-31 23:59:59"},
                                     "data": {"total_incident": []}, "scale": "month_of_year"}], format='json')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.content)[0][0]['count'], 2)
            self.assertEqual(json.loads(response.content)[1][0]['count'], 2)
            self.assertEqual(json.loads(response.content)[2][0]['count'], 2)
        except Exception as e:
            print e.message

    def testYearScale(self):
        try:
            self.current_datetime += datetime.timedelta(weeks=1)

            for i in range(0, 2):
                for j in range(0, 3):
                    incident = IncidentFactory(resort=self.resort, assigned_to=self.user,
                                               incident_status=self.incidentStatus)
                    response = self.c.put('/api/v3/incidents/%s/' % incident.incident_id,
                                          {
                                              "field_52ca456962ba8": {
                                                  "lat": -27.059125784374054,
                                                  "long": 135,
                                                  "accuracy": 4
                                              },
                                              "dt_created": (
                                                  self.current_datetime + datetime.timedelta(days=j * 30,
                                                                                             weeks=i * 52)).strftime(
                                                  "%Y-%m-%d %H:%M:%S")
                                          }, format='json')

            response = self.c.post('/api/v3/reports/timeline/?resort_id=%s&date_from=%s' % (
                self.resort.resort_id, self.current_datetime.strftime("%Y-%m-%d 00:00:01")),
                                   [{"date": {"datefrom": "2014-01-01 00:00:01", "dateto": "2015-12-31 23:59:59"},
                                     "data": {"total_incident": []}, "scale": "year"}], format='json')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.content)[0][0]['count'], 3)
            self.assertEqual(json.loads(response.content)[1][0]['count'], 3)
        except Exception as e:
            print e.message
