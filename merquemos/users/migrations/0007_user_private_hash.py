# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-05 14:49
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20171004_1817'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='private_hash',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
    ]
