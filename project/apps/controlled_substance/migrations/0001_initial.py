# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.conf import settings
from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('incidents', '0015_auto_20160115_1629'),
        ('resorts', '0025_area_resortlocation'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('controlled_substance_audit_log_pk',
                 models.AutoField(serialize=False, verbose_name=b'controlled substance audit log pk', primary_key=True,
                                  db_column=b'controlled_substance_audit_log_pk')),
                ('controlled_substance_audit_log_id',
                 models.UUIDField(default=uuid.uuid4, verbose_name=b'controlled substance audit log id', editable=False,
                                  db_column=b'controlled_substance_audit_log_id')),
                ('log_entry', models.TextField(verbose_name=b'log entry', db_column=b'log_entry')),
                (
                'dt_added', models.DateTimeField(auto_now_add=True, verbose_name=b'date added', db_column=b'dt_added')),
                ('added_by_user',
                 models.ForeignKey(db_column=b'added_by_user', blank=True, to=settings.AUTH_USER_MODEL, null=True,
                                   verbose_name=b'added by user')),
                ('resort', models.ForeignKey(db_column=b'resort', verbose_name=b'resort', to='resorts.Resort')),
            ],
        ),
        migrations.CreateModel(
            name='ControlledSubstances',
            fields=[
                ('controlled_substance_pk',
                 models.AutoField(serialize=False, verbose_name=b'controlled substance pk', primary_key=True,
                                  db_column=b'controlled_substance_pk')),
                ('controlled_substance_id',
                 models.UUIDField(default=uuid.uuid4, verbose_name=b'controlled substance id', editable=False,
                                  db_column=b'controlled_substance_id')),
                ('controlled_substance_name',
                 models.CharField(max_length=140, null=True, verbose_name=b'controlled substance name',
                                  db_column=b'controlled_substance_name', blank=True)),
                ('controlled_substance_status',
                 models.IntegerField(default=0, verbose_name=b'controlled substance status',
                                     db_column=b'controlled_substance_status',
                                     choices=[(0, b'live'), (1, b'deleted')])),
                ('units', models.CharField(max_length=140, verbose_name=b'units', db_column=b'units')),
                ('incident_json_path_substance',
                 models.CharField(max_length=255, null=True, verbose_name=b'incident json path substance',
                                  db_column=b'incident_json_path_substance', blank=True)),
                ('incident_json_path_user',
                 models.CharField(max_length=255, null=True, verbose_name=b'incident json path user',
                                  db_column=b'incident_json_path_user', blank=True)),
                ('resort', models.ForeignKey(db_column=b'resort', verbose_name=b'resort', to='resorts.Resort')),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('controlled_substance_stock_pk',
                 models.AutoField(serialize=False, verbose_name=b'controlled substance stock pk', primary_key=True,
                                  db_column=b'controlled_substance_stock_pk')),
                ('controlled_substance_stock_id',
                 models.UUIDField(default=uuid.uuid4, verbose_name=b'controlled substance stock id', editable=False,
                                  db_column=b'controlled_substance_stock_id')),
                ('volume', models.FloatField(verbose_name=b'volume', db_column=b'volume')),
                ('dt_expiry',
                 models.DateTimeField(null=True, verbose_name=b'date of expiry', db_column=b'dt_expiry', blank=True)),
                (
                'dt_added', models.DateTimeField(auto_now_add=True, verbose_name=b'date added', db_column=b'dt_added')),
                ('dt_disposed',
                 models.DateTimeField(null=True, verbose_name=b'date disposed', db_column=b'dt_disposed', blank=True)),
                ('current_status',
                 models.IntegerField(default=0, verbose_name=b'current status', db_column=b'current_status',
                                     choices=[(0, b'in'), (1, b'out'), (2, b'used'), (3, b'disposed')])),
                ('added_by_user',
                 models.ForeignKey(related_name='added_by_user', db_column=b'added_by_user', blank=True,
                                   to=settings.AUTH_USER_MODEL, null=True, verbose_name=b'added by user')),
                ('controlled_substance',
                 models.ForeignKey(db_column=b'controlled_substance', verbose_name=b'controlled substance id',
                                   to='controlled_substance.ControlledSubstances')),
                ('disposed_by_user',
                 models.ForeignKey(related_name='disposed_by_user', db_column=b'disposed_by_user', blank=True,
                                   to=settings.AUTH_USER_MODEL, null=True, verbose_name=b'disposed by user')),
                ('location',
                 models.ForeignKey(db_column=b'location', verbose_name=b'location', to='resorts.ResortLocation')),
            ],
        ),
        migrations.CreateModel(
            name='StockAssignment',
            fields=[
                ('controlled_substance_stock_assignment_pk',
                 models.AutoField(serialize=False, verbose_name=b'stock assignment pk', primary_key=True,
                                  db_column=b'controlled_substance_stock_assignment_pk')),
                ('controlled_substance_stock_assignment_id',
                 models.UUIDField(default=uuid.uuid4, verbose_name=b'stock assignment id', editable=False,
                                  db_column=b'controlled_substance_stock_assignment_id')),
                (
                'dt_added', models.DateTimeField(auto_now_add=True, verbose_name=b'date added', db_column=b'dt_added')),
                ('controlled_substance_stock_assignment_status',
                 models.IntegerField(default=0, verbose_name=b'stock assignment status',
                                     db_column=b'controlled_substance_stock_assignment_status',
                                     choices=[(0, b'in'), (1, b'out'), (2, b'used')])),
                ('dt_used',
                 models.DateTimeField(null=True, verbose_name=b'date used', db_column=b'dt_used', blank=True)),
                ('controlled_substance_stock',
                 models.ForeignKey(db_column=b'controlled_substance_stock', verbose_name=b'controlled substance stock',
                                   to='controlled_substance.Stock')),
                ('incident_id_used',
                 models.ForeignKey(db_column=b'incident_id_used', blank=True, to='incidents.Incident', null=True,
                                   verbose_name=b'used for incident id')),
                ('user', models.ForeignKey(db_column=b'user', verbose_name=b'user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
