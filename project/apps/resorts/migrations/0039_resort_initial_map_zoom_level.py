# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apps.resorts.models


class Migration(migrations.Migration):

    dependencies = [
        ('resorts', '0038_update_incident_json'),
    ]

    operations = [
        migrations.AddField(
            model_name='resort',
            name='initial_map_zoom_level',
            field=models.IntegerField(default=18, validators=[apps.resorts.models.validate_zoom_level]),
        ),
    ]
