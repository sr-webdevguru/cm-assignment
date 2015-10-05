# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

import apps.resorts.models


class Migration(migrations.Migration):
    dependencies = [
        ('resorts', '0014_resort_default_unit_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resort',
            name='map_kml',
            field=models.FileField(max_length=255, upload_to=apps.resorts.models.get_upload_path, blank=True),
        ),
        migrations.AlterField(
            model_name='resort',
            name='report_form',
            field=models.FileField(upload_to=apps.resorts.models.get_upload_path, max_length=255,
                                   verbose_name=b'report form for resort', blank=True),
        ),
        migrations.AlterField(
            model_name='resort',
            name='resort_logo',
            field=models.FileField(upload_to=apps.resorts.models.get_upload_path, max_length=255,
                                   verbose_name=b'resort logo', blank=True),
        ),
    ]
