# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('incidents', '0005_auto_20150503_0510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incidentnotes',
            name='note',
            field=models.TextField(null=True, verbose_name=b'note text', blank=True),
        ),
        migrations.AlterField(
            model_name='incidentnotes',
            name='note_date',
            field=models.DateTimeField(null=True, verbose_name=b'Date for Note creation', blank=True),
        ),
        migrations.AlterField(
            model_name='incidentnotes',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
