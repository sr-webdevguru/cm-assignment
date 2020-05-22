# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('incidents', '0004_auto_20150502_0528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statushistory',
            name='status_date',
            field=models.DateTimeField(),
        ),
    ]
