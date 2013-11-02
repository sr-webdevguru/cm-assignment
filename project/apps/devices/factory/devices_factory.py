import factory
from django.utils import timezone

from apps.custom_user.factory.user_factory import UserFactory
from apps.devices.models import Devices, Heartbeat


class DevicesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Devices
        django_get_or_create = {'device_id', }

    device_type = 'android'
    device_os = 'android'
    device_push_token = 'abcdefghijklmnopqrst123456789'
    device_state = 0
    device_user = UserFactory()


class HeartbeatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Heartbeat
        django_get_or_create = {'user', 'device'}

    user = UserFactory()
    device = DevicesFactory()
    heartbeat_datetime = timezone.now()
