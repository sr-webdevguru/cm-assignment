# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('resorts', '0018_resort_config_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='resort',
            name='default_unit_paper',
            field=models.IntegerField(default=0, blank=True, choices=[(0, b'A4'), (1, b'US Paper')]),
        ),
    ]
