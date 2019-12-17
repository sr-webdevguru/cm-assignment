# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('resorts', '0012_auto_20150619_0908'),
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='report_resort',
            field=models.ForeignKey(db_column=b'report_resort', to='resorts.Resort', null=True),
        ),
    ]
