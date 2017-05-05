# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('incidents', '0017_upload_existing_file_s3'),
    ]

    operations = [
        migrations.AddField(
            model_name='incidentaudit',
            name='prev_assigned_to',
            field=models.ForeignKey(related_name='incident_prev_assigned_user', default=None, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
