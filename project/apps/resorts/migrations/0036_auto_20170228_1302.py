# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apps.resorts.models
import storages.backends.s3boto3


class Migration(migrations.Migration):

    dependencies = [
        ('resorts', '0035_migrate_patient_data_kms'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resort',
            name='map_kml',
            field=models.FileField(storage=storages.backends.s3boto3.S3Boto3Storage(bucket=b's3-org-us-dev'), max_length=255, upload_to=apps.resorts.models.get_upload_path, blank=True),
        ),
        migrations.AlterField(
            model_name='resort',
            name='report_form',
            field=models.FileField(storage=storages.backends.s3boto3.S3Boto3Storage(bucket=b's3-org-us-dev'), upload_to=apps.resorts.models.get_upload_path, max_length=255, verbose_name=b'report form for resort', blank=True),
        ),
        migrations.AlterField(
            model_name='resort',
            name='resort_logo',
            field=models.FileField(storage=storages.backends.s3boto3.S3Boto3Storage(bucket=b's3-org-us-dev'), upload_to=apps.resorts.models.get_upload_path, max_length=255, verbose_name=b'resort logo', blank=True),
        ),
    ]
