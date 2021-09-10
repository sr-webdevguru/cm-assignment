# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

from apps.controlled_substance.models import USED
from helper_functions import sort_drug_administered_by


def manipulate_drug_administered_by(apps, schema_editor):

    Resort = apps.get_model("resorts", "Resort")
    Stock = apps.get_model("controlled_substance", "Stock")
    StockAssignment = apps.get_model("controlled_substance", "StockAssignment")

    resorts = Resort.objects.all()

    for resort in resorts:
        try:
            drug_field = resort.incident_template['DashboardItems']['field_52ca42230a171']['Questions']['field_52d4800164f2e'][
                'RepeatingQuestions']
        except:
            continue

        for key, value in drug_field.iteritems():
            if key.startswith("drug_administered_by"):
                stock = ""
                for i, each_drug_administered_by in enumerate(drug_field[key]['Values']):
                    for stock_id, user_name in drug_field[key]['Values'][i].iteritems():
                        stock = Stock.objects.get(controlled_substance_stock_id=stock_id)

                        drug_field[key]['Values'][i][stock_id] = str(stock.controlled_substance_stock_pk) + " " + drug_field[key]['Values'][i][stock_id]

                used_stock = StockAssignment.objects.filter(controlled_substance_stock__controlled_substance=stock.controlled_substance, controlled_substance_stock_assignment_status=USED)

                if used_stock:
                    for each_stock in used_stock:
                        drug_field[key]['Values'].append({str(each_stock.controlled_substance_stock.controlled_substance_stock_id): "USED " + str(each_stock.controlled_substance_stock.controlled_substance_stock_pk) + " " + each_stock.user.name})
                drug_field[key]['Values'] = sort_drug_administered_by(drug_field[key]['Values'])

                print drug_field[key]['Values']
        resort.save()


class Migration(migrations.Migration):

    dependencies = [
        ('controlled_substance', '0004_auto_20160418_1559'),
    ]

    operations = [
        migrations.RunPython(manipulate_drug_administered_by)
    ]
