import factory
from django.contrib.auth import get_user_model

from apps.custom_user.models import UserRoles


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ('email',)

    email = 'duncan@sixfive.com'
    name = 'Duncan'
    password = factory.PostGenerationMethodCall('set_password', '1234')
    is_admin = False


class UserRolesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserRoles
        django_get_or_create = ('key',)

    role_id = factory.Sequence(int)
    key = 'patroller'
    order = 1
