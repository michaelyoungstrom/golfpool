# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-10 21:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0027_auto_20190310_2118'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playerevent',
            old_name='round_four_total_score',
            new_name='round_four_to_par',
        ),
        migrations.RenameField(
            model_name='playerevent',
            old_name='round_one_total_score',
            new_name='round_one_to_par',
        ),
        migrations.RenameField(
            model_name='playerevent',
            old_name='round_three_total_score',
            new_name='round_three_to_par',
        ),
        migrations.RenameField(
            model_name='playerevent',
            old_name='round_two_total_score',
            new_name='round_two_to_par',
        ),
    ]
