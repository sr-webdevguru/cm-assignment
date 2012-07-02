# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('custom_user', '0006_auto_20150823_0548'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='user_asset_management',
            field=models.BooleanField(default=False, verbose_name=b'user asset management'),
        ),
        migrations.AddField(
            model_name='users',
            name='user_controlled_substances',
            field=models.BooleanField(default=False, verbose_name=b'user controlled substances'),
        ),
    ]
