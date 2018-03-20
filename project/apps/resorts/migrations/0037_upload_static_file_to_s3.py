# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.files.base import File
from django.db import migrations


def upload_static_file_to_s3(apps, schema_editor):
    Resort = apps.get_model("resorts", "Resort")

    resorts = Resort.objects.all()

    for each_resort in resorts:
        if each_resort.resort_logo.name != '' and each_resort.resort_logo.name is not None:
            try:
                with open(each_resort.resort_logo.name) as logo_file:
                    each_resort.resort_logo = File(logo_file)
                    each_resort.save()
            except:
                print each_resort.resort_logo.name + " not found"
                
        if each_resort.report_form.name != '' and each_resort.report_form.name is not None:
            try:
                with open(each_resort.report_form.name) as report_file:
                    each_resort.report_form = File(report_file)
                    each_resort.save()
            except:
                print each_resort.report_form.name + " not found"

        if each_resort.map_kml.name != '' and each_resort.map_kml.name is not None:
            try:
                with open(each_resort.map_kml.name) as kml_file:
                    each_resort.map_kml = File(kml_file)
                    each_resort.save()
            except:
                print each_resort.map_kml.name + " not found"


class Migration(migrations.Migration):
    dependencies = [
        ('resorts', '0036_auto_20170228_1302'),
    ]

    operations = [
        migrations.RunPython(upload_static_file_to_s3),
    ]