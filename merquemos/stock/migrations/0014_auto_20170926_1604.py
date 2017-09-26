# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-26 21:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0013_store_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_products', to='stock.Category'),
        ),
    ]
