# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def update_resort_config(apps, schema_editor):
    Resort = apps.get_model("resorts", "Resort")

    middle_field = "Questions"

    for resort in Resort.objects.all():
        resort_config = resort.incident_template

        try:
            resort_config["DashboardItems"]["field_52ca41790a16c"][middle_field]["field_52dd8c049b005"][
                'Type'] = "decimal"
        except:
            pass

        try:
            resort_config["DashboardItems"]["field_52ca41790a16c"][middle_field]["field_52dd8bee9b004"][
                'Type'] = "decimal"
        except:
            pass

        try:
            resort_config["DashboardItems"]["field_52ca42550a175"][middle_field]["field_52ca4637cc0fe"][
                'Type'] = "decimal"
        except:
            pass

        try:
            resort_config["DashboardItems"]["field_52ca42550a175"][middle_field]["field_52ca461ccc0fd"][
                'Type'] = "decimal"
        except:
            pass

        resort.incident_template = resort_config
        resort.save()


class Migration(migrations.Migration):
    dependencies = [
        ('resorts', '0017_auto_20151013_0425'),
    ]

    operations = [
        migrations.RunPython(update_resort_config),
    ]
