# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-07 19:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0010_auto_20170902_0910'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount_percentage',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='storeparameter',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_parameters', to='stock.Store'),
        ),
    ]
