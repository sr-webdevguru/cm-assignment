# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resorts', '0033_auto_20160918_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='resort',
            name='enc_data_key',
            field=models.TextField(default=b''),
        ),
    ]
