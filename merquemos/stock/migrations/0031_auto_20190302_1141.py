# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-03-02 16:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0030_auto_20190302_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='pum_type',
            field=models.CharField(blank=True, choices=[('GR', 'Gramo'), ('KG', 'Kilogramo'), ('ML', 'Mililitro'), ('LT', 'Litro'), ('CM', 'Centimetro'), ('MT', 'Metro')], max_length=2, null=True, verbose_name='Unidad de medida'),
        ),
    ]
