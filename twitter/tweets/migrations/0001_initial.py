# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-01 09:27
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('deleted', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
