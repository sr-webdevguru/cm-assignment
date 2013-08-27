# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('incidents', '0009_remove_incidentaudit_incident_json'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='dt_created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
