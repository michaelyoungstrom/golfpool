# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-15 00:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0030_auto_20190315_0022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pool',
            name='players',
            field=models.ManyToManyField(to='players.Player'),
        ),
    ]