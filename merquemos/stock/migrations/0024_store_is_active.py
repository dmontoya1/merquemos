# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-10-20 13:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0023_auto_20181020_0838'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
