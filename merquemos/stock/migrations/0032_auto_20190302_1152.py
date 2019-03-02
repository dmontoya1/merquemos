# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-03-02 16:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0031_auto_20190302_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='pum_value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Precio por unidad de medida'),
        ),
    ]