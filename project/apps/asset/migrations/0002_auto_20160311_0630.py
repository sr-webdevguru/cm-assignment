# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('asset', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assets',
            name='asset_name',
            field=models.CharField(default='', max_length=140, verbose_name=b'asset name', db_column=b'asset_name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='assettype',
            name='asset_type_name',
            field=models.CharField(default='', max_length=140, verbose_name=b'asset type name',
                                   db_column=b'asset_type_name'),
            preserve_default=False,
        ),
    ]
