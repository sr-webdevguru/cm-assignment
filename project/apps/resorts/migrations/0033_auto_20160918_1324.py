# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resorts', '0032_userresortmap_user_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='resort',
            name='kms_cmk',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Customer Master Key for Resort', blank=True),
        ),
        migrations.AddField(
            model_name='resort',
            name='kms_enabled',
            field=models.BooleanField(default=False, verbose_name=b'KMS enabled for resort'),
        ),
    ]
