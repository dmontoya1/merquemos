# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from stock.models import Product

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    status = models.CharField(max_length=2)
    last_status_date = models.DateTimeField()

    class Meta:
        verbose_name = "Orden de compra"
        verbose_name_plural = "Ordenes de compra"
    
    def __str__(self):
        return str(self.pk)

class Item(models.Model):
    product = models.ForeignKey(Product)
    order = models.ForeignKey(Order)
    quantity = models.PositiveIntegerField()
    tax_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.pk)

class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    order = models.ForeignKey(Order)
    number = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Reseña de compra"
        verbose_name_plural = "Reseñas de compra"
    
    def __str__(self):
        return str(self.pk)

class DeliveryOrder(models.Model):
    order = models.ForeignKey(Order)
    payment_method = models.CharField(max_length=2)
    status = models.CharField(max_length=2)
    extra_details = models.TextField()
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Orden de entrega"
        verbose_name_plural = "Ordenes de entrega"
    
    def __str__(self):
        return str(self.pk)