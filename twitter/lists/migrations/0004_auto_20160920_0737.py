# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-20 07:37
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0003_auto_20160920_0736'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='member_names',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='list',
            name='subscriber_names',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), blank=True, null=True, size=None),
        ),
    ]