# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('resorts', '0005_auto_20150507_0845'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resort',
            old_name='map_long',
            new_name='map_lng',
        ),
        migrations.AlterField(
            model_name='resort',
            name='map_kml',
            field=models.FileField(upload_to=b'media', blank=True),
        ),
    ]
