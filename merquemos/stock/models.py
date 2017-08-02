# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from manager.models import City


class Store(models.Model):
    name = models.CharField(max_length=255, unique=True)
    legal_id_number = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to="stock/store/logos")
    city = models.ForeignKey(City)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Tienda"

    def __str__(self): 
        return str(self.name)

class StoreContact(models.Model):
    store = models.ForeignKey(Store)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    occupation = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Contacto"

    def __str__(self):
        return str(self.name)

class StoreHour(models.Model):
    DAY_CHOICES = (
        (1, 'Lunes'),
        (2, 'Martes'),
        (3, 'Miercoles'),
        (4, 'Jueves'),
        (5, 'Viernes'),
        (6, 'Sábado'),
        (7, 'Domingo'),
    )
    store = models.ForeignKey(Store)
    day = models.CharField(max_length=1, choices=DAY_CHOICES)
    open_time = models.TimeField()
    close_time = models.TimeField()

    class Meta:
        verbose_name = "Horario"
        unique_together = ('store', 'day')

    def __str__(self):
        return str(self.day.get_display_name())

class StoreParameter(models.Model):
    store = models.ForeignKey(Store)
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Parámetro de tienda"
        verbose_name_plural = "Parámetros de tiendas"

    def __str__(self):
        return "%s de %s" % self._meta.verbose_name_plural, str(self.store)

class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Marca"

    def __str__(self):
        return str(self.name)

class BrandStore(models.Model):
    brand = models.ForeignKey(Brand)
    store = models.ForeignKey(Store)

    class Meta:
        verbose_name = "Marca por tienda"
        verbose_name_plural = "Marcas por tiendas"
    
    def __str__(self):
        return '%s / %s' % self.brand, self.store

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Categoría"
    
    def __str__(self):
        return str(self.name)

class Product(models.Model):
    store = models.ForeignKey(Store)
    brand = models.ForeignKey(BrandStore)
    category = models.ForeignKey(Category)  
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField()
    tax_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Producto"
    
    def __str__(self):
        return str(self.name)

class Inventory(models.Model):
    product = models.ForeignKey(Product)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Inventario"
    
    def __str__(self):
        return self.product


    