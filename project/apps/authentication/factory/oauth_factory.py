import datetime

import factory
from django.utils import timezone
from rest_framework.authtoken.models import Token

from apps.custom_user.factory.user_factory import UserFactory
from oauth2_provider.models import AccessToken
from oauth2_provider.models import Application


class ApplicationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Application
        django_get_or_create = ('name',)

    name = "medic52"
    user = UserFactory()
    client_type = 'confidential'
    authorization_grant_type = 'client-credentials'


class AccessTokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AccessToken

    application = ApplicationFactory()
    expires = (lambda: timezone.now() + datetime.timedelta(seconds=1800))()
    token = 'CLIChvzSE5hPMGbUPpbMEWlkTxPH7O'


class TokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Token
        django_get_or_create = ('user',)

    user = UserFactory()
