# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-28 04:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0006_auto_20170920_2343'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]