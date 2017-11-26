# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('incidents', '0014_update_incident_number_to_float'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='assigned_to',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
