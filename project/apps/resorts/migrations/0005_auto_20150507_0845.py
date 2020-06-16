# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('resorts', '0004_auto_20150507_0558'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userresortmap',
            old_name='role_id',
            new_name='role',
        ),
    ]
