# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-27 04:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0014_auto_20181126_0244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerevent',
            name='round_four_to_par',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='playerevent',
            name='round_one_to_par',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='playerevent',
            name='round_three_to_par',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='playerevent',
            name='round_two_to_par',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
