# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('incidents', '0002_remove_incidenttemplate_language'),
    ]

    operations = [
        migrations.CreateModel(
            name='IncidentNotes',
            fields=[
                ('note_id', models.AutoField(serialize=False, primary_key=True)),
                ('note', models.TextField(verbose_name=b'note text')),
                ('note_date', models.DateTimeField(auto_now_add=True)),
                ('incident', models.ForeignKey(to='incidents.Incident')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StatusHistory',
            fields=[
                ('status_history_id', models.AutoField(serialize=False, primary_key=True)),
                ('status_date', models.DateTimeField(auto_now_add=True)),
                ('incident', models.ForeignKey(to='incidents.Incident')),
                ('status', models.ForeignKey(to='incidents.IncidentStatus')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
