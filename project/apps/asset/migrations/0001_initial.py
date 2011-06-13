# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('resorts', '0025_area_resortlocation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assets',
            fields=[
                ('asset_pk',
                 models.AutoField(serialize=False, verbose_name=b'asset pk', primary_key=True, db_column=b'asset_pk')),
                ('asset_id',
                 models.UUIDField(default=uuid.uuid4, verbose_name=b'asset id', editable=False, db_column=b'asset_id')),
                ('asset_name',
                 models.CharField(max_length=140, null=True, verbose_name=b'asset name', db_column=b'asset_name')),
                ('asset_status', models.IntegerField(default=0, verbose_name=b'asset status', db_column=b'asset_status',
                                                     choices=[(0, b'live'), (1, b'deleted')])),
            ],
        ),
        migrations.CreateModel(
            name='AssetType',
            fields=[
                ('asset_type_pk', models.AutoField(serialize=False, verbose_name=b'asset type pk', primary_key=True,
                                                   db_column=b'asset_type_pk')),
                ('asset_type_id', models.UUIDField(default=uuid.uuid4, verbose_name=b'asset type id', editable=False,
                                                   db_column=b'asset_type_id')),
                ('asset_type_name', models.CharField(max_length=140, null=True, verbose_name=b'asset type name',
                                                     db_column=b'asset_type_name')),
                ('asset_type_status',
                 models.IntegerField(default=0, verbose_name=b'asset type status', db_column=b'asset_type_status',
                                     choices=[(0, b'live'), (1, b'deleted')])),
                ('resort', models.ForeignKey(db_column=b'resort', verbose_name=b'resort', to='resorts.Resort')),
            ],
        ),
        migrations.AddField(
            model_name='assets',
            name='asset_type',
            field=models.ForeignKey(db_column=b'asset_type', verbose_name=b'asset type', to='asset.AssetType'),
        ),
        migrations.AddField(
            model_name='assets',
            name='location',
            field=models.ForeignKey(db_column=b'location', verbose_name=b'location', to='resorts.ResortLocation'),
        ),
        migrations.AddField(
            model_name='assets',
            name='resort',
            field=models.ForeignKey(db_column=b'resort', verbose_name=b'resort', to='resorts.Resort'),
        ),
    ]
