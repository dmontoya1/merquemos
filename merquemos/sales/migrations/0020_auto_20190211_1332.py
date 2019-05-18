# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-02-11 18:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0019_auto_20190211_1249'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='delivery_option',
        ),
        migrations.RemoveField(
            model_name='order',
            name='delivery_time',
        ),
        migrations.AddField(
            model_name='deliveryorder',
            name='delivery_option',
            field=models.CharField(choices=[('IN', 'Inmediato'), ('PM', 'Programado')], default='IN', max_length=2, verbose_name='Opci\xf3n de entrega'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deliveryorder',
            name='delivery_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Tiempo de entrega'),
        ),
    ]
