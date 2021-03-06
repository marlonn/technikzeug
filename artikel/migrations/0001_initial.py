# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-22 22:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artikel',
            fields=[
                ('a_id', models.AutoField(db_column='a-id', primary_key=True, serialize=False)),
                ('titel', models.CharField(max_length=512)),
                ('text', models.TextField(max_length=10000)),
                ('tags', models.CharField(max_length=256)),
                ('datum', models.DateField()),
                ('bild', models.CharField(blank=True, max_length=128)),
            ],
            options={
                'db_table': 'artikel',
                'managed': True,
            },
        ),
    ]
