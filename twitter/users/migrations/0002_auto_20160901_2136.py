# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-01 21:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='twitteruser',
            old_name='updated',
            new_name='time',
        ),
    ]
