# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('devices', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devices',
            name='device_push_token',
            field=models.CharField(max_length=100, verbose_name=b'device push token', blank=True),
        ),
    ]
