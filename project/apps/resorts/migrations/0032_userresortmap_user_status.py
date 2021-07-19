# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resorts', '0031_auto_20160510_1158'),
    ]

    operations = [
        migrations.AddField(
            model_name='userresortmap',
            name='user_status',
            field=models.IntegerField(default=0, choices=[(0, b'Active'), (1, b'Archived'), (2, b'Deleted')]),
        ),
    ]
