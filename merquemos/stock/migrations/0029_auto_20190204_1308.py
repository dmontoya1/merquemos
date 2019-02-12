# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-02-04 18:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0028_store_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='address',
            field=models.CharField(max_length=255, verbose_name='Direcci\xf3n'),
        ),
        migrations.AlterField(
            model_name='store',
            name='app_cover',
            field=models.ImageField(blank=True, null=True, upload_to='stock/stores/app_covers/', verbose_name='Im\xe1gen para M\xf3vil'),
        ),
        migrations.AlterField(
            model_name='store',
            name='app_hex_code',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='C\xf3digo HEX color'),
        ),
        migrations.AlterField(
            model_name='store',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_stores', to='manager.City', verbose_name='Ciudad'),
        ),
        migrations.AlterField(
            model_name='store',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Tienda activa?'),
        ),
        migrations.AlterField(
            model_name='store',
            name='legal_id_number',
            field=models.CharField(max_length=255, unique=True, verbose_name='NIT'),
        ),
        migrations.AlterField(
            model_name='store',
            name='logo',
            field=models.ImageField(upload_to='stock/stores/logos/', verbose_name='logo'),
        ),
        migrations.AlterField(
            model_name='store',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='store',
            name='phone_number',
            field=models.CharField(max_length=255, verbose_name='N\xfamero telef\xf3nico'),
        ),
        migrations.AlterField(
            model_name='store',
            name='web_cover',
            field=models.ImageField(blank=True, null=True, upload_to='stock/stores/web_covers/', verbose_name='Im\xe1gen para Web'),
        ),
        migrations.AlterField(
            model_name='storeparameter',
            name='delivery_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Precio Domicilio'),
        ),
    ]