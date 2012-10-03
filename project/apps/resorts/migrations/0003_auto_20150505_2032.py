# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

import apps.resorts.models


class Migration(migrations.Migration):
    dependencies = [
        ('resorts', '0002_auto_20150505_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resort',
            name='network_key',
            field=models.CharField(default=apps.resorts.models.get_random_key, unique=True, max_length=255,
                                   verbose_name=b'resort network key'),
        ),
    ]
