# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('resorts', '0016_auto_20150903_0904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resort',
            name='default_unit_length',
            field=models.IntegerField(default=1, blank=True, choices=[(0, b'M'), (1, b'FT'), (2, b'CM')]),
        ),
    ]
