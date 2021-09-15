# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('custom_user', '0002_auto_20150504_0512'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='user_connected',
            field=models.IntegerField(default=0, verbose_name=b'device state'),
        ),
    ]
