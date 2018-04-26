# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
           name='Domains',
           fields=[
               ('domain_id', models.AutoField(serialize=False, primary_key=True)),
               ('domain', models.CharField(max_length=80)),
           ],
        ),
        migrations.CreateModel(
           name='Languages',
           fields=[
               ('language_id', models.AutoField(serialize=False, primary_key=True)),
               ('language_label', models.CharField(max_length=50)),
               ('language_code', models.CharField(max_length=20)),
           ],
        ),
        migrations.CreateModel(
           name='RoutingCompany',
           fields=[
               ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
               ('resort_token', models.CharField(unique=True, max_length=100)),
               ('resort_name', models.CharField(max_length=50)),
               ('domain', models.ForeignKey(to='routing.Domains')),
           ],
        ),
        migrations.CreateModel(
           name='RoutingUser',
           fields=[
               ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
               ('email', models.EmailField(max_length=254)),
               ('domain', models.ForeignKey(to='routing.Domains')),
           ],
        ),
    ]
