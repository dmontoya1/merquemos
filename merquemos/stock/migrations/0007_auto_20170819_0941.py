# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-19 14:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0006_inventory_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='logo',
            field=models.ImageField(upload_to='stock/stores/logos/'),
        ),
    ]
