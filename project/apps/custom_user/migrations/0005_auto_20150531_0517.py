# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('custom_user', '0004_auto_20150528_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='phone',
            field=models.CharField(max_length=20, null=True, verbose_name=b'user phone number', blank=True),
        ),
    ]
