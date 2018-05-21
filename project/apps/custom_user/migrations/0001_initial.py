# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('user_pk', models.AutoField(serialize=False, primary_key=True)),
                ('user_id', models.UUIDField(default=uuid.uuid4, verbose_name=b'user unique id', editable=False)),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name=b'user email')),
                ('phone', models.IntegerField(null=True, verbose_name=b'user phone number', blank=True)),
                ('name', models.CharField(max_length=254, verbose_name=b'user full name')),
                ('locale', models.CharField(default=b'en_US', max_length=10, verbose_name=b'user locale')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserRoles',
            fields=[
                ('role_id', models.AutoField(serialize=False, primary_key=True)),
                ('key', models.CharField(max_length=140, verbose_name=b'user role key id')),
                ('order', models.IntegerField(verbose_name=b'user role order')),
            ],
        ),
    ]
