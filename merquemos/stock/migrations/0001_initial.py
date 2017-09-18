# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-02 12:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('manager', '0003_auto_20170802_0550'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name': 'Marcas',
            },
        ),
        migrations.CreateModel(
            name='BrandStore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.Brand')),
            ],
            options={
                'verbose_name': 'Marca por tienda',
                'verbose_name_plural': 'Marcas por tiendas',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Categor\xeda',
            },
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
            ],
            options={
                'verbose_name': 'Inventario',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('tax_percentage', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('size', models.CharField(max_length=255)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.BrandStore')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.Category')),
            ],
            options={
                'verbose_name': 'Producto',
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('legal_id_number', models.CharField(max_length=255, unique=True)),
                ('logo', models.ImageField(upload_to='stock/store/logos')),
                ('address', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=255)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.City')),
            ],
            options={
                'verbose_name': 'Tienda',
            },
        ),
        migrations.CreateModel(
            name='StoreContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('occupation', models.CharField(max_length=255)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.Store')),
            ],
            options={
                'verbose_name': 'Contacto',
            },
        ),
        migrations.CreateModel(
            name='StoreHour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[(1, 'Lunes'), (2, 'Martes'), (3, 'Miercoles'), (4, 'Jueves'), (5, 'Viernes'), (6, 'S\xe1bado'), (7, 'Domingo')], max_length=1)),
                ('open_time', models.TimeField()),
                ('close_time', models.TimeField()),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.Store')),
            ],
            options={
                'verbose_name': 'Horario',
            },
        ),
        migrations.CreateModel(
            name='StoreParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.Store')),
            ],
            options={
                'verbose_name': 'Par\xe1metro',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.Store'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.Product'),
        ),
        migrations.AddField(
            model_name='brandstore',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.Store'),
        ),
        migrations.AlterUniqueTogether(
            name='storehour',
            unique_together=set([('store', 'day')]),
        ),
    ]