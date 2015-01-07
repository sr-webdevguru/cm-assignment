# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import ast
import json
import uuid

from django.db import models, migrations, connection


def migrate_incident_data(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Incident = apps.get_model("incidents", "Incident")
    cursor = connection.cursor()
    for incident in Incident.objects.all():
        try:
            incident_json = ast.literal_eval(incident.incident_json)
        except:
            try:
                incident_json = ast.literal_eval(str(json.loads(incident.incident_json)))
            except:
                incident_json = incident.incident_json

        if incident_json is not None:
            email = incident_json.get('email', '')
            incident_json.pop('email', None)

            phone = incident_json.get('phone', '')
            incident_json.pop('phone', None)

            dob = incident_json.get('dob', '')
            incident_json.pop('dob', None)

            sex = incident_json.get('sex', '')
            incident_json.pop('sex', None)

            name = incident_json.get('name', '')
            incident_json.pop('name', None)

            address = incident_json.get('address', '')
            incident_json.pop('address', None)

            suburb = incident_json.get('suburb', '')
            incident_json.pop('suburb', None)

            state = incident_json.get('state', '')
            incident_json.pop('state', None)

            country = incident_json.get('country', '')
            incident_json.pop('country', None)

            postcode = incident_json.get('postcode', '')
            incident_json.pop('postcode', None)

            cursor.execute("""INSERT INTO incidents_patients (
                            patient_id,
                            incident_id,
                            name,
                         sex,
                         address,
                         suburb,
                         state,
                         postcode,
                         country,
                         phone,
                         email,
                         dob
                        )
                        SELECT
                         v.patient_id,
                         v.incident_id,
                         pgp_pub_encrypt(v.name, keys.pubkey) As name,
                         v.sex,
                         pgp_pub_encrypt(v.address, keys.pubkey) As address,
                         pgp_pub_encrypt(v.suburb, keys.pubkey) As suburb,
                         pgp_pub_encrypt(v.state,keys.pubkey) As state,
                         pgp_pub_encrypt(v.postcode, keys.pubkey) As postcode,
                         v.country,
                         pgp_pub_encrypt(v.phone,keys.pubkey) As phone,
                         pgp_pub_encrypt(v.email, keys.pubkey) As email,
                          pgp_pub_encrypt(v.dob, keys.pubkey) As dob
                        FROM (
                          VALUES (
                           uuid_generate_v4(),
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s
                          )
                            ) AS v (
                           patient_id,
                           incident_id,
                           name,
                           sex,
                           address,
                           suburb,
                           state,
                           postcode,
                           country,
                           phone,
                           email,
                           dob
                          )
CROSS JOIN (SELECT dearmor('-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: GnuPG v2

mQENBFUfAXYBCAC8qjdz6A7ke1b9s2X6HtGIUt1esFt7CjKKJBIv4DqiUh3h4VYz
falFuzgmLNR2G05jnwRvRJs9T4pxRIVHT+6EjR65Nq8zqoEoyTJrT+YVCveU0Lrk
C1T4DrFF9YwCPIDAR0qO2hOHaNlpLdbWWRS5wX7xRnMIHnJR8qotRREIOXsCzDey
pQRbX7epnYgZGrtmsNQoJ9a0qCbUCp2dQi/FziWYEx4VDDyBA1D1wnENfgE56xmv
bLGe3QKGV6EGCaJfwbzgQ2+CfL7l0IoN4GL19zJJgY4NhXHKddazpyvQLT/tZtLj
gGInjpWw5yP01lBmk4WfqoJj/6O9DY+fs9l7ABEBAAG0SE1lZGljNTIgRGV2ZWxv
cG1lbnQgKERldmVsb3BtZW50IFBISSBlbmNyeXB0aW9uIGtleSkgPGhlbGxvQG1l
ZGljNTIuY29tPokBOAQTAQIAIgUCVR8BdgIbAwYLCQgHAwIGFQgCCQoLBBYCAwEC
HgECF4AACgkQ3EZQ1fwMxtlTiAf9FrDXs2YJUTaXn7uDFM56PtZVSK142cK5pC+v
s8id4NspfFCvZnC0M0OfbGQxsb08A/XkrGYywcwW3sWw/aAsPIBnYmzuArFv43jk
/CT7HeYNByvoiYsVhubYXm+0kHTAJy2/N5LJvyfTC2Gc6u0LgLQeJxUIt/jcq+mM
msgyAwNpnxuw8O8lVO+luDzQ9wawQX/MFVOCWIPzu3ov4wwFCOu2EL+Q4JucT7W1
CgHO0T0JzlE6WMKLSojC7Ze8Bqs/FRi7o59/s2NvOWIA6F393uEj0IWhMkK7d1mB
qtpHKoj3N+W3XkAVYgh+wjCPyuXCDU2oifafvRPQVOYwAxEG67kBDQRVHwF2AQgA
pDiKHj4y5rqQWnH3IOzhj4UUrynZftRpWnIQsh0i6exUqovOv8YQqx0DK7j5ohoR
Rigek19Rx3wrXCSoeuUbF+PRNz80YKqgrZj7obmup+V5sW48XYEqiFYaLYV54NcA
ppSqYHtPvJBCo9Vq9OmBrgO5HTrXpUG41E6xPE/U6WVuH7ZoK9sfFIL0myEyBZI6
YvucCOt/2UC0mtPom0Pag2UAcSk0BfM/fxoMDzT3peETvZz7IEAlluTTio4NDlmL
L7nQU+G2/FyQdd4qA/8Nt0GCw7U97H0Xr3Mo59PpSelmL58srlnOgI81YKAH4Vzx
Uh/QYi3tsPBg09ajyGOFIwARAQABiQEfBBgBAgAJBQJVHwF2AhsMAAoJENxGUNX8
DMbZR8YIALCykMl+Gje74ABRb2bTwgS6dPXeQfNFLI9gwqd2WLusbCNI5PDu5SkP
g79UHDqX0AjHDeVN58ZswFaGfrAAZeLLKog4IjrQYbgxJDT8jJ4EASnxnvCz2fcz
exHtOqRyEE15vUMbbxjh9W5qMV/rgstZaUwjQg9ElwXjUIbW+KpoD9wFBqaEgrFU
Jjtq+C/uTTRBrq6uVcWLOVMzvwX8kLX98wVSYFcp/q76N+PtYpVlokNL4x5GePvP
O1poImtW8+QoJlGSpCxSCGO1+DotT8BSW4A4bFhavdF0vQe23E1dXN1k0tpOeua9
DMyJynFv2Z1YcfAf45kDk0QX2AOj/3A=
=Ymij
-----END PGP PUBLIC KEY BLOCK-----') As pubkey
) As keys;""", [incident.incident_pk, name, sex, address, suburb, state, postcode, country, phone, email, dob])

            cursor.execute("UPDATE incidents_incident SET incident_data = %s WHERE incident_pk = %s",
                           [json.dumps(incident_json), incident.incident_pk])
    cursor.close()


class Migration(migrations.Migration):
    dependencies = [
        ('incidents', '0007_custom_sql'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patients',
            fields=[
                ('incident_patient_id', models.AutoField(serialize=False, primary_key=True)),
                ('patient_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('incident', models.ForeignKey(to='incidents.Incident')),
            ],
        ),
        migrations.RunSQL(
            "ALTER TABLE incidents_patients ADD dob BYTEA, ADD email BYTEA, ADD phone BYTEA, ADD sex VARCHAR(10), ADD name BYTEA, ADD address BYTEA, ADD suburb BYTEA, ADD state BYTEA, ADD country VARCHAR(255), ADD postcode BYTEA;"),
        migrations.RunPython(migrate_incident_data)
    ]
