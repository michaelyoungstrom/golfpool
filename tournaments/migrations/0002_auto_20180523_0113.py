# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-23 01:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='start_date',
            field=models.DateField(),
        ),
    ]