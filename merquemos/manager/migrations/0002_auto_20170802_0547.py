# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-02 10:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apppolicy',
            options={'verbose_name': 'Poliza de usuario', 'verbose_name_plural': 'Polizas de usuario'},
        ),
    ]
