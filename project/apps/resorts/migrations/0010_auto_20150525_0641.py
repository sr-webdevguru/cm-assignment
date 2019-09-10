# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('resorts', '0009_auto_20150524_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resort',
            name='default_unit_distance',
            field=models.IntegerField(default=0, blank=True, choices=[(0, b'KM'), (1, b'M')]),
        ),
        migrations.AlterField(
            model_name='resort',
            name='default_unit_length',
            field=models.IntegerField(default=1, blank=True, choices=[(0, b'M'), (1, b'FT')]),
        ),
        migrations.AlterField(
            model_name='resort',
            name='default_unit_temp',
            field=models.IntegerField(default=0, blank=True, choices=[(0, b'C'), (1, b'F')]),
        ),
        migrations.AlterField(
            model_name='resort',
            name='print_on_device',
            field=models.IntegerField(default=0, blank=True, choices=[(1, b'Yes'), (0, b'No')]),
        ),
    ]
