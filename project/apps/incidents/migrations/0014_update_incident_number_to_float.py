# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.db import migrations, connection

from apps.incidents.utils import dictfetchall


def update_incident_values(apps, schema_editor):
    cursor = connection.cursor()

    cursor.execute("""SELECT incident_pk, incident_data
FROM incidents_incident""")
    data = dictfetchall(cursor)

    for id, val in enumerate(data):
        incident_data = val['incident_data']

        try:
            incident_data["field_52dd8c049b005"] = float(incident_data["field_52dd8c049b005"])
        except:
            pass

        try:
            incident_data["field_52dd8bee9b004"] = float(incident_data["field_52dd8bee9b004"])
        except:
            pass

        try:
            incident_data["field_52ca4637cc0fe"] = float(incident_data["field_52ca4637cc0fe"])
        except:
            pass

        try:
            incident_data["field_52ca461ccc0fd"] = float(incident_data["field_52ca461ccc0fd"])
        except:
            pass

        cursor.execute("UPDATE incidents_incident SET incident_data = %s WHERE incident_pk = %s",
                       [json.dumps(incident_data), val['incident_pk']])

    cursor.close()


def update_incident_audit_values(apps, schema_editor):
    cursor = connection.cursor()

    cursor.execute("""SELECT audit_id, incident_data
FROM incidents_incidentaudit""")
    data = dictfetchall(cursor)

    for id, val in enumerate(data):
        incident_data = val['incident_data']

        try:
            incident_data["field_52dd8c049b005"] = float(incident_data["field_52dd8c049b005"])
        except:
            pass

        try:
            incident_data["field_52dd8bee9b004"] = float(incident_data["field_52dd8bee9b004"])
        except:
            pass

        try:
            incident_data["field_52ca4637cc0fe"] = float(incident_data["field_52ca4637cc0fe"])
        except:
            pass

        try:
            incident_data["field_52ca461ccc0fd"] = float(incident_data["field_52ca461ccc0fd"])
        except:
            pass

        cursor.execute("UPDATE incidents_incidentaudit SET incident_data = %s WHERE audit_id = %s",
                       [json.dumps(incident_data), val['audit_id']])

    cursor.close()


class Migration(migrations.Migration):
    dependencies = [
        ('incidents', '0013_replace_values'),
    ]

    operations = [
        migrations.RunPython(update_incident_values),
        migrations.RunPython(update_incident_audit_values)
    ]
