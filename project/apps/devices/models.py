import uuid

from django.db import models

from medic52.settings.common import AUTH_USER_MODEL

LIVE = 0
DELETION = 1
PENDING_DELETION = 2

DeviceState = (
    (LIVE, 'live'),
    (DELETION, 'deletion'),
    (PENDING_DELETION, 'pending_deletion')
)


class Devices(models.Model):
    device_pk = models.AutoField(primary_key=True)
    device_id = models.UUIDField(verbose_name="device unique id", default=uuid.uuid4, editable=False)
    device_type = models.CharField(verbose_name="device type", max_length=255)
    device_os = models.CharField(verbose_name="device os", max_length=255)
    device_push_token = models.CharField(verbose_name="device push token", max_length=100, blank=True)
    device_state = models.IntegerField(choices=DeviceState, verbose_name="device state", default=LIVE)
    device_user = models.ForeignKey(AUTH_USER_MODEL, verbose_name="owner of device")


class Heartbeat(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, verbose_name="user")
    device = models.ForeignKey(Devices, verbose_name="device")
    heartbeat_datetime = models.DateTimeField(verbose_name="heartbeat datetime", null=True)
