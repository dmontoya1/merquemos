# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-02 14:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0009_category_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='app_cover',
            field=models.ImageField(blank=True, null=True, upload_to='stock/stores/app_covers/'),
        ),
        migrations.AddField(
            model_name='store',
            name='app_hex_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
