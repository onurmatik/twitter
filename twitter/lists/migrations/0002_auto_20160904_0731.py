# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-04 07:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='list',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='list',
            name='slug',
        ),
    ]