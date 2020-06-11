# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('custom_user', '0003_users_user_connected'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='user_connected',
            field=models.IntegerField(default=0, verbose_name=b'user connected state',
                                      choices=[(0, b'solo'), (1, b'network')]),
        ),
    ]
