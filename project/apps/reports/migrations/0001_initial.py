# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.conf import settings
from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('report_pk', models.AutoField(serialize=False, primary_key=True, db_column=b'report_pk')),
                ('report_id', models.UUIDField(default=uuid.uuid4, verbose_name=b'report unique id', editable=False,
                                               db_column=b'report_id')),
                ('global_status',
                 models.IntegerField(default=0, verbose_name=b'report global status', db_column=b'global_status')),
                ('report_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, db_column=b'report_user')),
            ],
        ),
        migrations.RunSQL("ALTER TABLE reports_report ADD report_config JSON;"),
    ]
