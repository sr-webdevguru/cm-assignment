import json

from rest_framework.test import APITestCase, APIClient

from apps.authentication.factory.oauth_factory import ApplicationFactory, TokenFactory
from apps.custom_user.factory.user_factory import UserFactory, UserRolesFactory
from apps.resorts.factory.resort_factory import IncidentTemplateFactory, ResortFactory, UserResortMapFactory
from apps.routing.factory.routing_factory import DomainFactory, RoutingCompanyFactory, RoutingUserFactory, \
    LanguagesFactory
from apps.routing.models import Domains, RoutingCompany, RoutingUser, Languages


class RoutingTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.application = ApplicationFactory()
        self.domain = DomainFactory(domain_id=1)
        self.domain = DomainFactory(domain_id=2, domain='api-dev-au.medic52.com', is_active=True)
        self.domain = DomainFactory(domain='testserver', is_active=True)
        self.incidentTemplate = IncidentTemplateFactory(template_id=1)
        self.resort = ResortFactory(resort_name='Vanilla Ski', license_expiry_date='2018-04-01T00:00:00', licenses=5)
        self.userRoles = UserRolesFactory()
        self.userRoles = UserRolesFactory(role_id=2, key='dispatcher', order=2)
        self.userRoles = UserRolesFactory(role_id=3, key='manager', order=3)
        self.user_resort_map = UserResortMapFactory(role_id=3, user=self.user, resort=self.resort)
        self.routing_company = RoutingCompanyFactory()
        self.routing_user = RoutingUserFactory()
        self.languages = LanguagesFactory()
        self.c = APIClient()
        self.token = TokenFactory(user=self.user)

    def testMobileDiscover(self):
        # print self.domain.pk
        response = self.client.post('/oauth/access_token/',
                                    {'grant_type': 'client_credentials', 'client_id': self.application.client_id,
                                     'client_secret': self.application.client_secret})
        # print response.content
        self.access_token = json.loads(response.content)['access_token']
        self.c.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.c.post('/api/v3/auth/login/', {'email': self.user.email, 'password': '1234'}, format='json')
        response = self.c.post('/api/v3/auth/discover/', {'email': self.user.email}, format='json')
        # print response
        self.assertEqual(response.status_code, 200)

        response = self.c.post('/api/v3/auth/discover/', {'email': 'jerol.mail.com'}, format='json')
        self.assertEqual(response.status_code, 400)

        response = self.c.post('/api/v3/auth/discover/', {'email': 'jerol@mail.com'}, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.post('/api/v3/auth/discover/', {'resort_network_key': 'ZmY4YzZm'}, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.post('/api/v3/auth/discover/', {'resort_network_key': 'ZmY4YzZmx'}, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.post('/api/v3/auth/discover/', {'resort_name': 'Toggenburg'}, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.post('/api/v3/auth/discover/', {'resort_name': 'Vanilla Ski'}, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.post('/api/v3/auth/discover/', {'country': 'Australia'}, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.post('/api/v3/auth/discover/', {'country': 'US'}, format='json')
        self.assertEqual(response.status_code, 200)

    def testModels(self):
        self.assertEqual(Domains.objects.get(pk=1).__unicode__(), 'api-dev-us.medic52.com')

        self.assertEqual(RoutingCompany.objects.get(resort_token='ZmY4YzZm').__unicode__(), 'Vanilla Ski')

        self.assertEqual(RoutingUser.objects.get(email='duncan@sixfive.com').__unicode__(), 'duncan@sixfive.com')

        self.assertEqual(Languages.objects.get(language_label='English').__unicode__(), 'English')
