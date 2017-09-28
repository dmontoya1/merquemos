# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.db.models import Sum

from stock.models import Product
from users.models import Address

from .helpers import get_value_from_percentage


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

    def get_items(self):
        return self.related_items.all().order_by('pk')
    
    def has_items(self):
        if self.get_items().count() > 0:
            return True
        return False

    def get_item_quantity(self):
        if self.has_items():
            return self.get_items().aggregate(Sum('quantity'))['quantity__sum']
        return 0

    def get_total_no_tax(self):
        if self.has_items():
            total = 0
            for item in self.get_items():
                tax = item.product.get_price_no_tax()
                total = total + tax
        return 0

    def get_total_tax(self):
        total = 0
        for item in self.get_items():
            tax = item.get_tax_value()
            total = total + tax
        return total
    
    def get_total_with_tax(self):
        return self.get_total_no_tax() + self.get_total_tax() + self.get_delivery_price()

    def get_delivery_price(self):
        if self.has_items():
            return self.get_items().last().product.store.get_delivery_price()
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
        self.price = self.product.get_price()
        self.total = int(self.product.get_price()) * self.quantity
        super(Item, self).save(*args, **kwargs)

    def get_tax_value(self):
        percentage = get_value_from_percentage(self.tax_percentage)
        return self.price*percentage

class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    order = models.OneToOneField(Order)
    number = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Reseña de compra"
        verbose_name_plural = "Reseñas de compra"
    
    def __str__(self):
        return str(self.pk)

class DeliveryOrder(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('CS', 'Cash'),
        ('PS', 'POS'),
    )
    STATUS_CHOICES = (
        ('RN', 'Running'),
        ('DV', 'Delivered'),
        ('CA', 'Cancelled'),
    )

    order = models.OneToOneField(Order)
    payment_method = models.CharField(max_length=2, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='RN')
    address = models.ForeignKey(Address, null=True, blank=True)
    extra_details = models.TextField(null=True, blank=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = "Orden de entrega"
        verbose_name_plural = "Ordenes de entrega"
    
    def __str__(self):
        return str(self.pk)