# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-25 01:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0002_auto_20180523_0113'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='number_of_pools',
            field=models.IntegerField(default=8),
            preserve_default=False,
        ),
    ]
