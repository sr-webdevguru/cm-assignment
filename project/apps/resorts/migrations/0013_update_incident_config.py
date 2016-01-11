# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

change_list = ["1st_day", "1st_week", "1_4_weeks", "4_8_weeks", "8_weeks", "short", "long", "10_lessons", "1_5_lessons",
               "6_10_lessons", "4wd_vehicle", "1-5_lessons", "6-10_lessons", "1-4_weeks", "4-8_weeks", "firstst_week"]
change_replace = {"1st_day": "first_day", "1st_week": "first_week", "1_4_weeks": "one_to_four_weeks",
                  "4_8_weeks": "four_to_eight_weeks", "8_weeks": "eight_weeks", "short": "short_guard",
                  "long": "long_guard", "10_lessons": "ten_lessons", "1_5_lessons": "one_five_lessons",
                  "6_10_lessons": "six_ten_lessons", "4wd_vehicle": "fourwd_vehicle", "1-5_lessons": "one_five_lessons",
                  "6-10_lessons": "six_ten_lessons", "1-4_weeks": "one_to_four_weeks",
                  "4-8_weeks": "four_to_eight_weeks",
                  "firstst_week": "first_week"}


def update_resort_config(apps, schema_editor):
    Resort = apps.get_model("resorts", "Resort")

    for resort in Resort.objects.all():
        resort_config = resort.incident_template

        try:
            for id, value in enumerate(
                    resort_config['DashboardItems']['field_52ca41790a16c']['Questions']['field_52ca3dfcac438'][
                        'Values']):
                if value[value.keys()[0]] in change_list:
                    value[value.keys()[0]] = change_replace[value[value.keys()[0]]]
        except:
            pass

        try:
            for id, value in enumerate(
                    resort_config['DashboardItems']['field_52ca41790a16c']['Questions']['field_52d483dceb786'][
                        'Values']):
                if value[value.keys()[0]] in change_list:
                    value[value.keys()[0]] = change_replace[value[value.keys()[0]]]
        except:
            pass

        try:
            for id, value in enumerate(
                    resort_config['DashboardItems']['field_52ca41790a16c']['Questions']['field_52d488615b642'][
                        'Values']):
                if value[value.keys()[0]] in change_list:
                    value[value.keys()[0]] = change_replace[value[value.keys()[0]]]
        except:
            pass

        try:
            for id, value in enumerate(
                    resort_config['DashboardItems']['field_52ca425e0a176']['Questions']['field_52ca4c34ef1a1'][
                        'Values']):
                if value[value.keys()[0]] in change_list:
                    value[value.keys()[0]] = change_replace[value[value.keys()[0]]]
        except:
            pass

        try:
            for id, value in enumerate(
                    resort_config['DashboardItems']['field_52ca41c50a16f']['Questions']['field_52ca453862ba6'][
                        'Values']):
                if value.keys()[0] == "????":
                    resort_config['DashboardItems']['field_52ca41c50a16f']['Questions']['field_52ca453862ba6'][
                        'Values'][id] = {"1431": "xc_trail"}
        except:
            pass

        resort.incident_template = resort_config
        resort.save()


class Migration(migrations.Migration):
    dependencies = [
        ('resorts', '0012_auto_20150619_0908'),
    ]

    operations = [
        migrations.RunPython(update_resort_config),
    ]
