# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def fix_radio_buttons(apps, schema_editor):
    fields = [
        [
            'field_52ca426c0a178', [
                'field_5334b101c8779',
                'field_53c386190a2dd',
                'field_52dd8a24e95a6',
                'field_539158b37814e'
            ],
        ],
        [
            'field_52ca41790a16c', [
                'field_52ca437b62b9c',
                'field_52ca43f362ba0',
                'field_52ca430462b9a',
                'field_52ca429c62b98',
                'field_52ca405959d2c',
                'field_52ca3fcc59d29',
                'field_52ca431e62b9b'
            ],
        ]
    ]
    Resorts = apps.get_model('resorts', 'Resort')
    for resort in Resorts.objects.all():
        if type(resort.incident_template) != dict:
            continue
        for field in fields:
            if field[0] not in resort.incident_template['DashboardItems']:
                continue
            if 'Questions' not in resort.incident_template['DashboardItems'][field[0]]:
                continue
            for question in field[1]:
                if question not in resort.incident_template['DashboardItems'][field[0]]["Questions"]:
                    continue
                resort.incident_template['DashboardItems'][field[0]]["Questions"][question]["Default"] = "unknown"
                resort.incident_template['DashboardItems'][field[0]]["Questions"][question]["Type"] = "radio_button"
                resort.incident_template['DashboardItems'][field[0]]["Questions"][question]["Values"].append({"unknown": "unknown"})
        resort.save()
    return

class Migration(migrations.Migration):


    dependencies = [
        ('resorts', '0039_resort_initial_map_zoom_level'),
    ]

    operations = [
        migrations.RunPython(fix_radio_buttons),
    ]
