# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-06-06 15:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0020_auto_20171005_1926'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='barcode',
            field=models.TextField(blank=True, null=True),
        ),
    ]