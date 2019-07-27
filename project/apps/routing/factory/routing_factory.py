import factory

from apps.custom_user.factory.user_factory import UserFactory
from apps.routing.models import Domains
from apps.routing.models import RoutingCompany, Languages
from apps.routing.models import RoutingUser


class DomainFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Domains
        django_get_or_create = ('domain',)

    domain_id = factory.Sequence(int)
    domain = 'api-dev-us.medic52.com'
    # laravel_domain = 'api-php-dev-us.medic52.com'
    is_active = True


class RoutingUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RoutingUser
        django_get_or_create = ('email', 'domain')

    email = UserFactory().email
    domain = DomainFactory()


class RoutingCompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RoutingCompany
        django_get_or_create = ('resort_token',)

    resort_token = "ZmY4YzZm"
    resort_name = "Vanilla Ski"
    domain = DomainFactory()


class LanguagesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Languages
        django_get_or_create = ('language_label',)

    language_id = 1
    language_label = 'English'
    language_code = 'Eng'
