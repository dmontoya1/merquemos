# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-29 16:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0008_rating_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='rating',
            name='number',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
