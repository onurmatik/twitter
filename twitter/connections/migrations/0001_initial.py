# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-17 02:48
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Followers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(db_index=True)),
                ('ids', django.contrib.postgres.fields.ArrayField(base_field=models.BigIntegerField(), size=None)),
                ('next_cursor', models.CharField(db_index=True, max_length=20)),
                ('previous_cursor', models.CharField(db_index=True, max_length=20)),
                ('time', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(db_index=True)),
                ('ids', django.contrib.postgres.fields.ArrayField(base_field=models.BigIntegerField(), size=None)),
                ('next_cursor', models.CharField(db_index=True, max_length=20)),
                ('previous_cursor', models.CharField(db_index=True, max_length=20)),
                ('time', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
