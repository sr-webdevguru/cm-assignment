# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('resorts', '0007_auto_20150523_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resort',
            name='default_unit_distance',
            field=models.IntegerField(blank=True, choices=[(0, b'KM'), (1, b'M')]),
        ),
    ]
