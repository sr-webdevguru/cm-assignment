# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('resorts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resort',
            name='network_key',
            field=models.UUIDField(default=uuid.uuid4, verbose_name=b'resort network key'),
        ),
    ]
