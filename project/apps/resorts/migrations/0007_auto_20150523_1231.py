# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

import apps.resorts.models


class Migration(migrations.Migration):
    dependencies = [
        ('resorts', '0006_auto_20150523_0925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resort',
            name='image',
            field=models.FileField(upload_to=apps.resorts.models.get_upload_path, verbose_name=b'resort logo',
                                   blank=True),
        ),
        migrations.AlterField(
            model_name='resort',
            name='map_kml',
            field=models.FileField(upload_to=apps.resorts.models.get_upload_path, blank=True),
        ),
        migrations.AlterField(
            model_name='resort',
            name='report_form',
            field=models.FileField(upload_to=apps.resorts.models.get_upload_path,
                                   verbose_name=b'report form for resort', blank=True),
        ),
    ]
