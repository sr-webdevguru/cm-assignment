# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from django.conf import settings
from django.db import migrations
from validators.uuid import uuid

from helper_functions import create_s3_client


def upload_file_to_s3(apps, schema_editor):
    Resort = apps.get_model("resorts", "Resort")

    # Create s3 client with provided credential
    client = create_s3_client()

    # Media directory where all media files are located
    media_path = os.path.join(settings.MEDIA_ROOT, 'media')

    # Iterate through each of the media directory
    # First level describes resort_id
    for each_dir in os.listdir(media_path):
        if uuid(each_dir):
            media_incident_path = os.path.join(media_path, each_dir)
            # Interate through second level which describes incident_id
            for each_incident_dir in os.listdir(media_incident_path):
                if uuid(each_incident_dir):
                    for each_file in os.listdir(os.path.join(media_incident_path, each_incident_dir)):
                        try:
                            # Fetch the resort to check KMS settings
                            resort = Resort.objects.get(resort_id=each_dir)

                            # Use global KMS Key for Encryption
                            kms_key = settings.GLOBAL_KMS_KEY_ID

                            # If resort has its own CMK then use it instead of global one
                            if resort.kms_enabled and resort.kms_cmk != "" and (resort.kms_cmk is not None):
                                kms_key = resort.kms_cmk
                            if os.path.isfile(os.path.join(media_incident_path, each_incident_dir, each_file)):
                                with open(os.path.join(media_incident_path, each_incident_dir, each_file)) as file_to_upload:
                                    response = client.put_object(Body=file_to_upload, Bucket=settings.BUCKET_NAME, Key="%s/%s/%s" % (each_dir, each_incident_dir, each_file), ServerSideEncryption="aws:kms", SSEKMSKeyId=kms_key)
                        except:
                            pass


class Migration(migrations.Migration):
    dependencies = [
        ('incidents', '0016_auto_20160321_1336'),
    ]

    operations = [
        migrations.RunPython(upload_file_to_s3),
    ]