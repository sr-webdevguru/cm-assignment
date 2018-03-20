# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('controlled_substance', '0002_auto_20160224_1131'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='controlledsubstances',
            name='incident_json_path_substance',
        ),
        migrations.RemoveField(
            model_name='controlledsubstances',
            name='incident_json_path_user',
        ),
        migrations.AlterField(
            model_name='controlledsubstances',
            name='controlled_substance_name',
            field=models.CharField(default='', max_length=140, verbose_name=b'controlled substance name',
                                   db_column=b'controlled_substance_name'),
            preserve_default=False,
        ),
    ]
