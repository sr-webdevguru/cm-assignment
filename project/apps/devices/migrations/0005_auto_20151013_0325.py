# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('devices', '0004_auto_20150531_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devices',
            name='device_os',
            field=models.CharField(max_length=255, verbose_name=b'device os'),
        ),
        migrations.AlterField(
            model_name='devices',
            name='device_type',
            field=models.CharField(max_length=255, verbose_name=b'device type'),
        ),
    ]
