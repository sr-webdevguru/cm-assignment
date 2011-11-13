# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

import encrypted_fields.fields
import jsonfield.fields
from django.conf import settings
from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('routing', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('resorts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('gender_id', models.AutoField(serialize=False, primary_key=True)),
                ('key', models.CharField(max_length=140)),
            ],
        ),
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('incident_pk', models.AutoField(serialize=False, primary_key=True)),
                ('incident_id',
                 models.UUIDField(default=uuid.uuid4, verbose_name=b'incident unique id', editable=False)),
                ('dt_created', models.DateTimeField(auto_now_add=True)),
                ('dt_modified', models.DateTimeField(auto_now=True)),
                ('incident_json', encrypted_fields.fields.EncryptedTextField()),
                ('assigned_to', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='IncidentAudit',
            fields=[
                ('audit_id', models.AutoField(serialize=False, primary_key=True)),
                ('dt_created', models.DateTimeField(auto_now_add=True)),
                ('incident_json', encrypted_fields.fields.EncryptedTextField()),
                ('assigned_to', models.ForeignKey(related_name='incident_assigned_user', to=settings.AUTH_USER_MODEL)),
                ('changed_by', models.ForeignKey(related_name='incident_changed_user', to=settings.AUTH_USER_MODEL)),
                ('incident', models.ForeignKey(to='incidents.Incident')),
                ('resort', models.ForeignKey(to='resorts.Resort')),
            ],
        ),
        migrations.CreateModel(
            name='IncidentStatus',
            fields=[
                ('incident_status_id', models.AutoField(serialize=False, primary_key=True)),
                ('order', models.IntegerField()),
                ('color', models.CharField(max_length=10)),
                ('key', models.CharField(max_length=140)),
            ],
        ),
        migrations.CreateModel(
            name='IncidentTemplate',
            fields=[
                ('template_id', models.AutoField(serialize=False, primary_key=True)),
                ('json', jsonfield.fields.JSONField()),
                ('language', models.ForeignKey(to='routing.Languages')),
            ],
        ),
        migrations.CreateModel(
            name='IncidentTemplateExceptions',
            fields=[
                ('exception_id', models.AutoField(serialize=False, primary_key=True)),
                ('json', jsonfield.fields.JSONField()),
                ('type', models.IntegerField(default=0)),
                ('dt_updated', models.DateTimeField(auto_now=True)),
                ('resort', models.ForeignKey(to='resorts.Resort')),
            ],
        ),
        migrations.AddField(
            model_name='incident',
            name='incident_status',
            field=models.ForeignKey(verbose_name=b'incident status', to='incidents.IncidentStatus'),
        ),
        migrations.AddField(
            model_name='incident',
            name='resort',
            field=models.ForeignKey(to='resorts.Resort'),
        ),
    ]
