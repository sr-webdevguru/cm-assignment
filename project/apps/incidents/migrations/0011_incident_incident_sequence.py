# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('incidents', '0010_auto_20150619_0451'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='incident_sequence',
            field=models.IntegerField(default=0, verbose_name=b'sequential number for incident'),
        ),
    ]
