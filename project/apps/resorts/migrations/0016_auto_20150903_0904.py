# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('resorts', '0015_auto_20150827_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resort',
            name='timezone',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
