# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_data', models.TextField(verbose_name=b'content of language file in base64')),
                ('dt_created',
                 models.DateTimeField(auto_now_add=True, verbose_name=b'datetime of language file upload')),
            ],
        ),
    ]
