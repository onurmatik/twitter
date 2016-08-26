# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-26 08:23
from __future__ import unicode_literals

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('members', django.contrib.postgres.fields.ArrayField(base_field=models.BigIntegerField(), blank=True, null=True, size=None)),
                ('subscribers', django.contrib.postgres.fields.ArrayField(base_field=models.BigIntegerField(), blank=True, null=True, size=None)),
                ('owner', models.BigIntegerField(db_index=True)),
                ('slug', models.SlugField()),
            ],
            options={
                'ordering': ('-updated',),
            },
        ),
    ]
