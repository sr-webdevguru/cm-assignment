# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('devices', '0005_auto_20151013_0325'),
    ]

    operations = [
        migrations.CreateModel(
            name='Heartbeat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('heartbeat_datetime', models.DateTimeField(null=True, verbose_name=b'heartbeat datetime')),
            ],
        ),
        migrations.RemoveField(
            model_name='devices',
            name='device_heartbeat_date',
        ),
        migrations.AddField(
            model_name='heartbeat',
            name='device',
            field=models.ForeignKey(verbose_name=b'device', to='devices.Devices'),
        ),
        migrations.AddField(
            model_name='heartbeat',
            name='user',
            field=models.ForeignKey(verbose_name=b'user', to=settings.AUTH_USER_MODEL),
        ),
    ]
