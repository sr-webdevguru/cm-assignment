# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('resorts', '0026_auto_20160221_0621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resortlocation',
            name='location_name',
            field=models.CharField(default='', max_length=140, verbose_name=b'location name',
                                   db_column=b'location_name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='resortlocation',
            name='map_lat',
            field=models.FloatField(default=0.0, verbose_name=b'map lat', db_column=b'map_lat'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='resortlocation',
            name='map_long',
            field=models.FloatField(default=0.0, verbose_name=b'map long', db_column=b'map_long'),
            preserve_default=False,
        )
    ]
