# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-18 21:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fcm_django', '0003_auto_20170313_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fcmdevice',
            name='device_id',
            field=models.CharField(blank=True, db_index=True, help_text='Unique device identifier', max_length=255, null=True, verbose_name='Device ID'),
        ),
    ]
