# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import base64

from django.conf import settings
from django.db import migrations, connection

from helper_functions import replace_null


def migrate_encrypted_patient_info(apps, schema_editor):
    from apps.incidents.utils import dictfetchall
    from helper_functions import create_client

    Resort = apps.get_model("resorts", "Resort")

    client = create_client()
    response = client.generate_data_key(KeyId=settings.GLOBAL_KMS_KEY_ID, KeySpec='AES_256')
    cursor = connection.cursor()

    cursor.execute("""SELECT
  incident_patient_id,
  pgp_pub_decrypt(name, keys.privkey)     AS name,
  pgp_pub_decrypt(address, keys.privkey)  AS address,
  pgp_pub_decrypt(suburb, keys.privkey)   AS suburb,
  pgp_pub_decrypt(state, keys.privkey)    AS state,
  pgp_pub_decrypt(postcode, keys.privkey) AS postcode,
  pgp_pub_decrypt(phone, keys.privkey)    AS phone,
  pgp_pub_decrypt(email, keys.privkey)    AS email,
  pgp_pub_decrypt(dob, keys.privkey) AS dob
FROM incidents_patients
CROSS JOIN (SELECT dearmor(%s) As privkey) As keys;""", [settings.GPG_PRIVATE_KEY, ])

    data = dictfetchall(cursor)

    for each_data in data:
        each_data = replace_null(each_data)
        cursor.execute("""UPDATE incidents_patients SET
                            name = pgp_sym_encrypt(v.name, keys.datakey, 'compress-algo=1, cipher-algo=aes256'),
                         address = pgp_sym_encrypt(v.address, keys.datakey, 'compress-algo=1, cipher-algo=aes256'),
                         suburb = pgp_sym_encrypt(v.suburb, keys.datakey, 'compress-algo=1, cipher-algo=aes256'),
                         state = pgp_sym_encrypt(v.state,keys.datakey, 'compress-algo=1, cipher-algo=aes256'),
                         postcode = pgp_sym_encrypt(v.postcode, keys.datakey, 'compress-algo=1, cipher-algo=aes256'),
                         phone = pgp_sym_encrypt(v.phone,keys.datakey, 'compress-algo=1, cipher-algo=aes256'),
                         email = pgp_sym_encrypt(v.email, keys.datakey, 'compress-algo=1, cipher-algo=aes256'),
                         dob = pgp_sym_encrypt(v.dob, keys.datakey, 'compress-algo=1, cipher-algo=aes256')
                        FROM (
                          VALUES (
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
                           name,
                           address,
                           suburb,
                           state,
                           postcode,
                           phone,
                           email,
                           dob
                          )
CROSS JOIN ( SELECT %s::TEXT AS datakey) AS keys
WHERE incidents_patients.incident_patient_id = %s;""", [each_data['name'], each_data['address'],
                                                        each_data['suburb'], each_data['state'], each_data['postcode'],
                                                        each_data['phone'], each_data['email'],
                                                        each_data['dob'], base64.b64encode(response['Plaintext']),
                                                        each_data['incident_patient_id']])

    resorts = Resort.objects.all().update(enc_data_key=base64.b64encode(response['CiphertextBlob']))
    cursor.close()


class Migration(migrations.Migration):
    dependencies = [
        ('resorts', '0034_resort_enc_data_key'),
    ]

    operations = [
        migrations.RunPython(migrate_encrypted_patient_info)
    ]
