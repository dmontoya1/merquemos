# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-19 22:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0012_auto_20170907_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]