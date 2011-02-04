# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('resorts', '0003_auto_20150505_2032'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userresortmap',
            old_name='role',
            new_name='role_id',
        ),
    ]
