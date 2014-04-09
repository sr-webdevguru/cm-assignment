# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('resorts', '0008_auto_20150524_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resort',
            name='default_unit_length',
            field=models.IntegerField(blank=True, choices=[(0, b'M'), (1, b'FT')]),
        ),
        migrations.AlterField(
            model_name='resort',
            name='default_unit_temp',
            field=models.IntegerField(blank=True, choices=[(0, b'C'), (1, b'F')]),
        ),
        migrations.AlterField(
            model_name='resort',
            name='map_type',
            field=models.IntegerField(default=1, blank=True, choices=[(0, b'Google Earth'), (1, b'Google Map')]),
        ),
        migrations.AlterField(
            model_name='resort',
            name='print_on_device',
            field=models.IntegerField(blank=True, choices=[(0, b'Yes'), (1, b'No')]),
        ),
    ]
