# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-04 23:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20171004_1506'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'ordering': ['-pk'], 'verbose_name': 'Direcci\xf3n', 'verbose_name_plural': 'Direcciones'},
        ),
    ]
