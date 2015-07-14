# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def update_resort_config(apps, schema_editor):
    Resort = apps.get_model("resorts", "Resort")


    for resort in Resort.objects.all():
        resort.dispatch_field_choice = [
            {
                "field_key": "name"
            },
            {
                "field_key": "phone"
            },
            {
                "field_key": "field_52d4798f6d227____body_part"
            },
            {
                "field_key": "field_52d48077a16be"
            }
        ]
        resort.save()


class Migration(migrations.Migration):
    dependencies = [
        ('resorts', '0029_auto_20160425_0517'),
    ]

    operations = [
        migrations.RunPython(update_resort_config),
    ]
