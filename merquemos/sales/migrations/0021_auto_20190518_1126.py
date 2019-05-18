# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-05-18 16:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0020_auto_20190211_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryorder',
            name='delivery_option',
            field=models.CharField(choices=[('IN', 'Inmediato'), ('PM', 'Programado'), ('PO', 'Recoger en el punto')], max_length=2, verbose_name='Opci\xf3n de entrega'),
        ),
    ]
