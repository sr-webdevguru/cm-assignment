# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import ast
import json

from django.db import migrations, connection


def migrate_incidentaudit_data(apps, schema_editor):
    IncidentAudit = apps.get_model("incidents", "IncidentAudit")
    cursor = connection.cursor()
    for incident_audit in IncidentAudit.objects.all():
        try:
            incident_json = ast.literal_eval(incident_audit.incident_json)
        except:
            try:
                incident_json = ast.literal_eval(str(json.loads(incident_audit.incident_json)))
            except:
                incident_json = incident_audit.incident_json
        cursor.execute("UPDATE incidents_incidentaudit SET incident_data = %s WHERE audit_id = %s",
                       [json.dumps(incident_json), incident_audit.audit_id])
    cursor.close()


class Migration(migrations.Migration):
    dependencies = [
        ('incidents', '0008_patients'),
    ]

    operations = [
        migrations.RunSQL("ALTER TABLE incidents_incidentaudit ADD incident_data JSON;"),
        migrations.RunPython(migrate_incidentaudit_data),
        migrations.RemoveField(
            model_name='incidentaudit',
            name='incident_json',
        ),
    ]
