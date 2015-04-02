# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def fix_radio_buttons(apps, schema_editor):
    resort_exceptions = ['caddb640-85e1-4431-bebc-3a75c3a69e88', '44338daf-0716-4562-a2f0-370a5bdaad96', 'ed75906a-9234-4163-825e-b8070a56c17a', '8819368a-9824-416e-a8b3-367159e0775f']

    Resorts = apps.get_model('resorts', 'Resort')
    for resort in Resorts.objects.all():
        if resort.resort_id.urn[9:] in resort_exceptions:
            continue
        if type(resort.incident_template) != dict:
            continue
        if 'DashboardItems' not in resort.incident_template:
            continue
        if 'field_52d47aac9bd13' not in resort.incident_template['DashboardItems']:
            continue
        if 'RepeatingQuestions' not in resort.incident_template['DashboardItems']['field_52d47aac9bd13']:
            continue
        if 'incident_role' not in resort.incident_template['DashboardItems']['field_52d47aac9bd13']['RepeatingQuestions']:
            continue
        resort.incident_template['DashboardItems']['field_52d47aac9bd13']['RepeatingQuestions']['incident_role']['Values'].append({"173": "transport_assist"})
        resort.incident_template['DashboardItems']['field_52d47aac9bd13']['RepeatingQuestions']['incident_role']['Values'].append({"174": "base_assist"})
        resort.save()

class Migration(migrations.Migration):

    dependencies = [
        ('resorts', '0040_auto_20170525_0553'),
    ]

    operations = [
        migrations.RunPython(fix_radio_buttons),
    ]
