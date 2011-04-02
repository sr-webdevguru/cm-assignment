# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('resorts', '0024_resort_datetime_format'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('area_pk',
                 models.AutoField(serialize=False, verbose_name=b'area pk', primary_key=True, db_column=b'area_pk')),
                ('area_id', models.UUIDField(default=uuid.uuid4, verbose_name=b'area id', db_column=b'area_id')),
                ('area_name',
                 models.CharField(max_length=140, null=True, verbose_name=b'area name', db_column=b'area_name',
                                  blank=True)),
                ('area_status', models.IntegerField(default=0, verbose_name=b'area status', db_column=b'area_status',
                                                    choices=[(0, b'live'), (1, b'deleted')])),
                ('resort', models.ForeignKey(db_column=b'resort', verbose_name=b'resort', to='resorts.Resort')),
            ],
        ),
        migrations.CreateModel(
            name='ResortLocation',
            fields=[
                ('location_pk', models.AutoField(serialize=False, verbose_name=b'location pk', primary_key=True,
                                                 db_column=b'location_pk')),
                ('location_id',
                 models.UUIDField(default=uuid.uuid4, verbose_name=b'location id', db_column=b'location_id')),
                ('location_name', models.CharField(max_length=140, null=True, verbose_name=b'location name',
                                                   db_column=b'location_name')),
                ('map_lat', models.FloatField(null=True, verbose_name=b'map lat', db_column=b'map_lat')),
                ('map_long', models.FloatField(null=True, verbose_name=b'map long', db_column=b'map_long')),
                ('location_status',
                 models.IntegerField(default=0, verbose_name=b'location status', db_column=b'location_status',
                                     choices=[(0, b'live'), (1, b'deleted')])),
                ('area', models.ForeignKey(db_column=b'area', verbose_name=b'area', to='resorts.Area')),
                ('resort', models.ForeignKey(db_column=b'resort', verbose_name=b'resort', to='resorts.Resort')),
            ],
        ),
    ]
