# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.conf import settings
from django.db import models
from django.db.models import F
from django.urls import reverse_lazy
from django.utils.text import slugify

from manager.models import City


class Store(models.Model):
    name = models.CharField(max_length=255, unique=True)
    legal_id_number = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to="stock/stores/logos/")
    city = models.ForeignKey(City)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    app_cover = models.ImageField(
        upload_to="stock/stores/app_covers/",
        null=True,
        blank=True
    )
    app_hex_code = models.CharField(max_length=10, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    class Meta:
        verbose_name = "Tienda"

    def __str__(self): 
        return str(self.name)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Store, self).save(*args, **kwargs)

    def get_delivery_price(self):
        if self.related_parameters.all().count() > 0:
            params = self.related_parameters.all().last()
            return params.delivery_price
        return 0
    
    @models.permalink
    def get_absolute_url(self):
        return reverse_lazy('webclient:store', args=(self.city.name, self.slug))

    def is_open(self):
        if self.related_hours.all().count() > 0:
            return True
        return False

class StoreContact(models.Model):
    store = models.ForeignKey(Store, related_name='related_contacts')
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
    store = models.ForeignKey(Store, related_name='related_hours')
    day = models.CharField(max_length=1, choices=DAY_CHOICES)
    open_time = models.TimeField()
    close_time = models.TimeField()

    class Meta:
        verbose_name = "Horario"
        unique_together = ('store', 'day')

    def __str__(self):
        return str(self.day.get_display_name())

class StoreParameter(models.Model):
    store = models.ForeignKey(Store, related_name='related_parameters')
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
        return str(self.brand)

class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True)

    class Meta:
        verbose_name = "Categoría"
    
    def __str__(self):
        return str(self.name)
    
    def get_related_products(self):
        if self.parent is None:
            return self.related_products.all()
        return Product.objects.filter(category__parent=self)
        
class Product(models.Model):
    store = models.ForeignKey(Store)
    brand = models.ForeignKey(BrandStore)
    category = models.ForeignKey(Category, related_name='related_products')  
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="stock/products/images/", null=True, blank=True)
    tax_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=255)
    stock_quantity = models.PositiveIntegerField(editable=False, default=0)
    discount_percentage = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Producto"
    
    def __str__(self):
        return str(self.name)
    
    def has_discount(self):
        if self.discount_percentage > 0:
            return True
        return False
    
    def get_discount_value(self):
        return self.discount_percentage*self.price/100

    def get_price(self):
        if self.has_discount():
            return self.price - self.get_discount_value()
        return self.price
    
    def get_image_url(self):
        if self.image:
            return self.image.url
        return None

class Inventory(models.Model):
    product = models.ForeignKey(Product)
    quantity = models.PositiveIntegerField()
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)

    class Meta:
        verbose_name = "Inventario"
    
    def __str__(self):
        return str(self.quantity)

    def __init__(self, *args, **kwargs):
        super(Inventory, self).__init__(*args, **kwargs)
        #Save last quantity value 
        self.last_quantity = self.quantity

    def save(self, raw=False, *args, **kwargs):
        if raw is False:
            #Increase product stock quantity when Inventory object is saved
            print self.last_quantity
            self.product.stock_quantity = self.product.stock_quantity + self.quantity
            self.product.save()
            super(Inventory, self).save(*args, **kwargs)



    