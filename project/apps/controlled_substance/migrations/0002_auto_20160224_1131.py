# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('controlled_substance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockassignment',
            name='controlled_substance_stock',
            field=models.ForeignKey(db_column=b'controlled_substance_stock', verbose_name=b'controlled substance stock',
                                    to='controlled_substance.Stock', unique=True),
        ),
    ]
