# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('resorts', '0025_area_resortlocation'),
    ]

    operations = [
        migrations.AddField(
            model_name='resort',
            name='resort_asset_management',
            field=models.BooleanField(default=False, verbose_name=b'resort asset management'),
        ),
        migrations.AddField(
            model_name='resort',
            name='resort_controlled_substances',
            field=models.BooleanField(default=False, verbose_name=b'resort controlled substances'),
        ),
    ]
