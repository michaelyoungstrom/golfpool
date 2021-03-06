# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-28 01:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0003_tournament_number_of_pools'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='day_four_score_count',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tournament',
            name='day_one_score_count',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tournament',
            name='day_three_score_count',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tournament',
            name='day_two_score_count',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
