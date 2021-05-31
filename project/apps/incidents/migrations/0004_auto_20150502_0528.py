# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('incidents', '0003_incidentnotes_statushistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incidentnotes',
            name='note_date',
            field=models.DateTimeField(verbose_name=b'Date for Note creation'),
        ),
    ]
