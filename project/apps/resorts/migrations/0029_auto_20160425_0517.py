# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('resorts', '0028_auto_20160311_0630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resort',
            name='dispatch_field_choice',
            field=jsonfield.fields.JSONField(default=[{b'field_key': b'name'}, {b'field_key': b'phone'}, {b'field_key': b'field_52d4798f6d227____body_part'}, {b'field_key': b'field_52d48077a16be'}], verbose_name=b'choice for dispatch screen'),
        ),
    ]
