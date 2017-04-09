# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('custom_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userroles',
            name='key',
            field=models.CharField(max_length=140, verbose_name=b'user role key'),
        ),
    ]
