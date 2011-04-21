# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

import jsonfield.fields
from django.conf import settings
from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('custom_user', '0001_initial'),
        ('routing', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('country_id', models.AutoField(serialize=False, primary_key=True)),
                ('key', models.CharField(max_length=140, verbose_name=b'key for country')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('location_id', models.AutoField(serialize=False, primary_key=True)),
                ('key', models.CharField(max_length=140, verbose_name=b'key id for location')),
                ('country', models.ForeignKey(verbose_name=b'country of location', to='resorts.Country')),
            ],
        ),
        migrations.CreateModel(
            name='Resort',
            fields=[
                ('resort_pk', models.AutoField(serialize=False, primary_key=True)),
                ('resort_id', models.UUIDField(default=uuid.uuid4, verbose_name=b'resort unique id', editable=False)),
                ('resort_name', models.CharField(max_length=255, verbose_name=b'resort name')),
                ('website', models.URLField(verbose_name=b'resort website', blank=True)),
                ('network_key', models.UUIDField(default=uuid.uuid4, verbose_name=b'resort unique id')),
                ('license_expiry_date',
                 models.DateTimeField(null=True, verbose_name=b'resort expiry expiration date', blank=True)),
                ('licenses', models.IntegerField(null=True, verbose_name=b'licenses owned by resort', blank=True)),
                ('map_kml', models.CharField(max_length=255, blank=True)),
                ('map_type', models.IntegerField(default=1, blank=True)),
                ('report_form', models.TextField(verbose_name=b'report form for resort', blank=True)),
                ('print_on_device', models.IntegerField(default=0, blank=True)),
                ('map_lat', models.FloatField(null=True, blank=True)),
                ('map_long', models.FloatField(null=True, blank=True)),
                ('default_unit_temp', models.IntegerField(default=0, blank=True)),
                ('default_unit_length', models.IntegerField(default=0, blank=True)),
                ('default_unit_distance', models.IntegerField(default=0, blank=True)),
                ('timezone', models.CharField(max_length=25, blank=True)),
                ('image', models.TextField(verbose_name=b'resort logo', blank=True)),
                ('dt_modified', models.DateTimeField(auto_now=True)),
                ('incident_template',
                 jsonfield.fields.JSONField(verbose_name=b'Incident template for resort', blank=True)),
                ('domain_id', models.ForeignKey(to='routing.Domains', null=True)),
                ('location',
                 models.ForeignKey(verbose_name=b'resort location', blank=True, to='resorts.Location', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserResortMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('resort', models.ForeignKey(to='resorts.Resort')),
                ('role', models.ForeignKey(to='custom_user.UserRoles')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='userresortmap',
            unique_together=set([('user', 'resort')]),
        ),
    ]
