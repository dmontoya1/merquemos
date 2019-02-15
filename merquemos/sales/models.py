# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.conf import settings
from django.db import models
from django.db.models import Sum

from cent import Client
from fcm_django.models import FCMDevice

from stock.models import Product
from users.models import Address
from utils.models import ExportModelMixin


class Order(ExportModelMixin):
    STATUS_CHOICES = (
        ('PE', 'Pendiente'),
        ('AC', 'Recibida'),
        ('SH', 'Enviada'),
        ('CA', 'Cancelada'),
        ('DE', 'Entregada')
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="related_orders",
        verbose_name='Usuario'
    )
    delivery_price = models.DecimalField(
        'Precio del domicilio',
        max_digits=10,
        decimal_places=2,
        default=0,
        null=True,
        blank=True
    )
    status = models.CharField(
        'Estado',
        max_length=2,
        choices=STATUS_CHOICES,
        default='PE'
    )
    last_status_date = models.DateTimeField(
        'Fecha de última actualización de estado',
        auto_now_add=True
    )
    comments = models.TextField(
        'Comentarios',
        null=True, 
        blank=True
    )
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Orden de compra"
        verbose_name_plural = "Ordenes de compra"

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        devices = FCMDevice.objects.filter(user=self.user)
        try:
            if self.status == "CA" or self.status == "DE" or self.status == "SH":
                data ={
                    "order_id": self.pk,
                    "order_status": self.status
                }
                if devices.count() > 0:
                    devices.send_message(
                        title="Tu orden de Merquemos",
                        body="Tu orden ha sido " + self.get_status_display().lower(),
                        icon="",
                        data=data
                    )
                client = Client(settings.CENTRIFUGE_ADDRESS, settings.CENTRIFUGE_SECRET, timeout=1)
                client.publish("private:{}#{}".format(self.user.private_hash, self.user.pk), data)
        except:
            pass
        super(Order, self).save(*args, **kwargs)

    def get_rating(self):
        try:
            return self.rating.number
        except:
            return 0

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
        total = 0
        if self.has_items():
            for item in self.get_items():
                price = item.get_price_no_tax()
                total = total + price
        return total

    def get_total_tax(self):
        total = 0
        for item in self.get_items():
            tax = item.get_tax_value()
            total = total + tax
        return total
    
    def get_total_with_tax(self):
        return self.get_total_no_tax() + self.get_total_tax() + self.get_delivery_price()

    def get_total_without_delivery(self):
        return self.get_total_no_tax() + self.get_total_tax()

    def get_delivery_price(self):
        if self.has_items():
            if self.status == "PE":
                return self.get_items().last().product.store.get_delivery_price()
            else:
                return self.delivery_price
        return 0

    @property
    def get_store_id(self):
        if self.has_items():
            return self.related_items.last().product.store.id
        return False
    
    @property
    def get_store_name(self):
        if self.has_items():
            return self.related_items.last().product.store.name
        return "Sin establecimiento"


class Item(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name='Producto'
    )
    order = models.ForeignKey(
        Order,
        related_name="related_items",
        verbose_name='Orden'
    )
    quantity = models.PositiveIntegerField('Cantidad')
    tax_percentage = models.DecimalField(
        'Porcentaje de impuestos',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    price = models.DecimalField(
        'Precio',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    total = models.DecimalField(
        'Total',
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
        return self.tax_percentage*self.total/100

    def get_price_no_tax(self):
        return self.total - self.get_tax_value()


class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    order = models.OneToOneField(Order)
    number = models.PositiveIntegerField(default=0)
    comments = models.TextField(null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Reseña de compra"
        verbose_name_plural = "Reseñas de compra"

    def __str__(self):
        return str(self.pk)


class DeliveryOrder(models.Model):
    INMEDIATELY = 'IN'
    PROGRAMMED = 'PM'

    DELIVERY_CHOICES = (
        (INMEDIATELY, 'Inmediato'),
        (PROGRAMMED, 'Programado'),
    )

    PAYMENT_METHOD_CHOICES = (
        ('CS', 'Efectivo'),
        ('PS', 'Datáfono'),
    )
    STATUS_CHOICES = (
        ('RN', 'En ejecución'),
        ('DV', 'Entregado'),
        ('CA', 'Cancelado'),
    )

    order = models.OneToOneField(Order, related_name="delivery_order")
    payment_method = models.CharField('Método de pago', max_length=2, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField('Estado', max_length=2, choices=STATUS_CHOICES, default='RN')
    address = models.ForeignKey(Address, verbose_name='Dirección', null=True, blank=True)
    extra_details = models.TextField('Datos extra', null=True, blank=True)
    paid_amount = models.DecimalField('Valor pagado', max_digits=10, decimal_places=2, null=True, blank=True)
    delivery_option = models.CharField(
        'Opción de entrega',
        max_length=2,
        choices=DELIVERY_CHOICES
    )
    delivery_time = models.DateTimeField(
        'Tiempo de entrega',
        auto_now=False,
        auto_now_add=False,
        blank=True, null=True
    )

    class Meta:
        verbose_name = "Orden de entrega"
        verbose_name_plural = "Ordenes de entrega"

    def __str__(self):
        return str(self.pk)