# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-26 04:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0003_userevent_total_score_to_par'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userevent',
            old_name='playerEvents',
            new_name='player_events',
        ),
    ]
