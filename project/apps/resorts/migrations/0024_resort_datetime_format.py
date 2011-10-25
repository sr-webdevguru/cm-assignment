# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('resorts', '0023_auto_20151218_0446'),
    ]

    operations = [
        migrations.AddField(
            model_name='resort',
            name='datetime_format',
            field=models.IntegerField(default=1, blank=True,
                                      choices=[(0, b'mm/dd/yyyy hh:mm:ss'), (1, b'dd/mm/yyyy hh:mm:ss')]),
        ),
    ]
