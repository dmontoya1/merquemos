# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-10-20 13:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0008_city_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
