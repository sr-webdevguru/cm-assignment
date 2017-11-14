# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


def update_incident_template(apps, schema_editor):
    Resort = apps.get_model("resorts", "Resort")

    resorts = Resort.objects.all()

    # Updating field type in incident template
    fields_to_update = ['field_52dd8bee9b004', 'field_52dd8c049b005']
    update_type = {'field_52dd8bee9b004': 'height', 'field_52dd8c049b005': 'weight'}

    for each_resort in resorts:
        try:
            incident_template = each_resort.incident_template['DashboardItems']

            for key, val in incident_template.iteritems():
                if 'Questions' in val:
                    for key1, val1 in incident_template[key]['Questions'].iteritems():
                        if key1 in fields_to_update:
                            incident_template[key]['Questions'][key1]['Type'] = update_type[key1]

                elif 'RepeatingQuestions' in val:
                    for key1, val1 in incident_template[key]['RepeatingQuestions'].iteritems():
                        if 'Type' in val1:
                            if key1 in fields_to_update:
                                incident_template[key]['RepeatingQuestions'][key1]['Type'] = update_type[key1]

            each_resort.incident_template = {"DashboardItems": incident_template}
        except:
            pass

        # Updating default unit
        region = settings.BUCKET_NAME.split('-')[2]
        if region == 'us':
            each_resort.unit_format = 0
        elif region == 'au':
            each_resort.unit_format = 1
        each_resort.save()


class Migration(migrations.Migration):
    dependencies = [
        ('resorts', '0037_upload_static_file_to_s3'),
    ]

    operations = [
        migrations.RunPython(update_incident_template),
    ]