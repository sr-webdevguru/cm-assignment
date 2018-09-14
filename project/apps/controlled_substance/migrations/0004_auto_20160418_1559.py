# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0016_auto_20160321_1336'),
        ('controlled_substance', '0003_auto_20160311_0630'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockassignment',
            name='incident_id_used',
        ),
        migrations.AddField(
            model_name='stockassignment',
            name='incident_id',
            field=models.ForeignKey(db_column=b'incident_id', blank=True, to='incidents.Incident', null=True, verbose_name=b'used for incident id'),
        ),
    ]
