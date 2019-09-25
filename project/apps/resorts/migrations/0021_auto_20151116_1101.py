# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('resorts', '0020_auto_20151110_1323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resort',
            name='default_unit_distance',
        ),
        migrations.RemoveField(
            model_name='resort',
            name='default_unit_length',
        ),
        migrations.RemoveField(
            model_name='resort',
            name='default_unit_temp',
        ),
        migrations.RemoveField(
            model_name='resort',
            name='default_unit_weight',
        ),
        migrations.AddField(
            model_name='resort',
            name='unit_format',
            field=models.IntegerField(default=0, blank=True, choices=[(0, b'Imperial'), (1, b'Metric')]),
        ),
    ]
