# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-03-02 16:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0029_auto_20190204_1308'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='pum_type',
            field=models.CharField(blank=True, choices=[('GR', 'Gramo'), ('ML', 'Mililitro'), ('CM', 'Centimetro')], max_length=2, null=True, verbose_name='Unidad de medida'),
        ),
        migrations.AddField(
            model_name='product',
            name='pum_value',
            field=models.PositiveIntegerField(default=0, verbose_name='Precio por unidad de medida'),
        ),
        migrations.AlterField(
            model_name='store',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_store', to=settings.AUTH_USER_MODEL, verbose_name='Administrador'),
        ),
    ]
