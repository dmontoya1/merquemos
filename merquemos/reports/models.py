# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from stock.models import Product
from sales.models import Order, DeliveryOrder, Rating


class OrderSummary(Order):
    class Meta:
        proxy = True
        verbose_name = 'Reporte de venta'
        verbose_name_plural = 'Reportes de ventas'


class DeliveryOrderSummary(DeliveryOrder):
    class Meta:
        proxy = True
        verbose_name = 'Reporte de entrega'
        verbose_name_plural = 'Reportes de entregas'


class RatingSummary(Rating):
    class Meta:
        proxy = True
        verbose_name = 'Reporte de calificacion'
        verbose_name_plural = 'Reportes de calificaciones'


class ProductSummary(Product):
    class Meta:
        proxy = True
        verbose_name = 'Reporte de producto'
        verbose_name_plural = 'Reportes de productos'
