# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('resorts', '0021_auto_20151116_1101'),
        ('oauth2_provider', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResortOauthApp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, verbose_name=b'is application active ?')),
                ('oauth_app', models.ForeignKey(verbose_name=b'oauth application associated with resort',
                                                to='oauth2_provider.Application')),
                ('resort', models.ForeignKey(verbose_name=b'resort associated with oauth app', to='resorts.Resort')),
            ],
        ),
    ]
