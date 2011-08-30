# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resorts', '0030_update_default_for_existing_resort'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resort',
            name='datetime_format',
            field=models.IntegerField(default=1, blank=True, choices=[(0, b'MM/DD/YYYY HH:mm:ss'), (1, b'DD/MM/YYYY HH:mm:ss')]),
        ),
    ]
