# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('incidents', '0011_incident_incident_sequence'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='incidentstatus',
            options={'ordering': ['key']},
        ),
    ]
