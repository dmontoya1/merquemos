# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-05 14:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20171005_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='private_hash',
            field=models.UUIDField(editable=False),
        ),
    ]