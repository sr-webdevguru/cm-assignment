# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.db import migrations, connection

from apps.incidents.utils import dictfetchall


def update_incident(apps, schema_editor):
    Incident = apps.get_model("incidents", "Incident")

    cursor = connection.cursor()

    cursor.execute("""SELECT incident_pk, incident_data
FROM incidents_incident
WHERE (incident_data ->> 'field_52ca453862ba6') = '????'""")
    data = dictfetchall(cursor)

    for id, val in enumerate(data):
        incident_data = val['incident_data']
        incident_data['field_52ca453862ba6'] = "1431"
        cursor.execute("UPDATE incidents_incident SET incident_data = %s WHERE incident_pk = %s",
                       [json.dumps(incident_data), val['incident_pk']])


class Migration(migrations.Migration):
    dependencies = [
        ('incidents', '0012_auto_20150823_0548'),
    ]

    operations = [
        migrations.RunPython(update_incident)
    ]
