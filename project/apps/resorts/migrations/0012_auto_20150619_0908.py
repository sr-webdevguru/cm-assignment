# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('resorts', '0011_auto_20150531_0822'),
    ]

    operations = [
        migrations.AddField(
            model_name='resort',
            name='season_start_date',
            field=models.DateField(default=datetime.date.today, verbose_name=b'season start date'),
        ),
        migrations.AddField(
            model_name='resort',
            name='use_sequential_incident_id',
            field=models.IntegerField(default=0, verbose_name=b'Use sequential incident id',
                                      choices=[(0, b'OFF'), (1, b'ON')]),
        ),
    ]
