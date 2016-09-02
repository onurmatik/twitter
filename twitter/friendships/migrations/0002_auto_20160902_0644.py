# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-02 06:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friendships', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendship',
            name='next_cursor',
            field=models.CharField(db_index=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='friendship',
            name='previous_cursor',
            field=models.CharField(db_index=True, max_length=20),
        ),
    ]
