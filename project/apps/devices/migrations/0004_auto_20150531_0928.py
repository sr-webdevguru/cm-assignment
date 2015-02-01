# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('devices', '0003_remove_devices_device_connected'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devices',
            name='device_state',
            field=models.IntegerField(default=0, verbose_name=b'device state',
                                      choices=[(0, b'live'), (1, b'deletion'), (2, b'pending_deletion')]),
        ),
    ]
