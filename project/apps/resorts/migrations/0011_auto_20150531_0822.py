# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('resorts', '0010_auto_20150525_0641'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resort',
            old_name='image',
            new_name='resort_logo',
        ),
    ]
