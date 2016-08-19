# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import uuid

from django.conf import settings
from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Devices',
            fields=[
                ('device_pk', models.AutoField(serialize=False, primary_key=True)),
                ('device_id', models.UUIDField(default=uuid.uuid4, verbose_name=b'device unique id', editable=False)),
                ('device_type', models.CharField(max_length=20, verbose_name=b'device type')),
                ('device_os', models.CharField(max_length=20, verbose_name=b'device os')),
                ('device_push_token', models.CharField(max_length=100, verbose_name=b'device push token')),
                ('device_state', models.IntegerField(default=0, verbose_name=b'device state')),
                ('device_connected', models.IntegerField(default=0, verbose_name=b'device connected')),
                ('device_heartbeat_date',
                 models.DateTimeField(default=datetime.datetime.now, verbose_name=b'device heartbeat date')),
                ('device_user', models.ForeignKey(verbose_name=b'owner of device', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
