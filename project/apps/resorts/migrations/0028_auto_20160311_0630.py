# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('resorts', '0027_auto_20160311_0608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='area_name',
            field=models.CharField(default='', max_length=140, verbose_name=b'area name', db_column=b'area_name'),
            preserve_default=False,
        ),
    ]
