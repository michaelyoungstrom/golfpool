# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-26 06:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0005_userevent_tournament'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userevent',
            name='tournament',
        ),
    ]