# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-06-13 23:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0007_auto_20170928_0012'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
