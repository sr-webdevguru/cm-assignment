# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('resorts', '0013_update_incident_config'),
    ]

    operations = [
        migrations.AddField(
            model_name='resort',
            name='default_unit_weight',
            field=models.IntegerField(default=0, blank=True, choices=[(0, b'KG'), (1, b'LB')]),
        ),
    ]
