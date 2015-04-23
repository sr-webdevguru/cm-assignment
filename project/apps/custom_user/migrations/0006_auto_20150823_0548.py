# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('custom_user', '0005_auto_20150531_0517'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='users',
            options={'ordering': ['name']},
        ),
    ]
