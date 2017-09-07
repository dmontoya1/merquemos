# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.db.models import Sum
from stock.models import Product

class Order(models.Model):
    STATUS_CHOICES = (
        ('PE', 'Pending'),
        ('AC', 'Accepted'),
        ('CA', 'Canceled'),
        ('DE', 'Delivered')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='PE')
    last_status_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Orden de compra"
        verbose_name_plural = "Ordenes de compra"
    
    def __str__(self):
        return str(self.pk)

    def get_item_quantity(self):
        return self.related_items.all().count()

    def get_total(self):
        if self.related_items.all().count() > 0:
            result = self.related_items.all().aggregate(Sum('total'))
            return result['total__sum']
        return 0

class Item(models.Model):
    product = models.ForeignKey(Product)
    order = models.ForeignKey(Order, related_name="related_items")
    quantity = models.PositiveIntegerField()
    tax_percentage = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        self.tax_percentage = self.product.tax_percentage
        self.price = self.product.price
        self.total = int(self.product.price) * self.quantity
        super(Item, self).save(*args, **kwargs)

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