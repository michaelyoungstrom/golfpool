# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-09 02:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0006_tournament_is_open'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tournament',
            old_name='entry_fee',
            new_name='par',
        ),
        migrations.RemoveField(
            model_name='tournament',
            name='id',
        ),
        migrations.AddField(
            model_name='tournament',
            name='tournament_id',
            field=models.IntegerField(default=None, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]