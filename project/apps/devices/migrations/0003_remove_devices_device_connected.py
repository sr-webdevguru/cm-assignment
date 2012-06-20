# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('devices', '0002_auto_20150508_0514'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devices',
            name='device_connected',
        ),
    ]
