# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-25 00:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0002_auto_20180523_0113'),
        ('players', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerevent',
            name='tournament',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='tournaments.Tournament'),
            preserve_default=False,
        ),
    ]
