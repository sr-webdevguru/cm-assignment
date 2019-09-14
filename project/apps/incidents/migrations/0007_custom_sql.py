# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('incidents', '0006_auto_20150605_1931'),
    ]

    operations = [
        migrations.RunSQL("ALTER TABLE incidents_incident ADD incident_data JSON;")
    ]
