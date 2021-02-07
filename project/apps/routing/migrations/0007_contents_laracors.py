# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def set_laravel_domains(apps, schema_editor):
    return


class Migration(migrations.Migration):

    dependencies = [
        ('routing', '0006_merge'),
    ]

    operations = [
        migrations.RunPython(set_laravel_domains),
    ]
