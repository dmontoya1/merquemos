# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import (
    Order, Item, Rating,
    DeliveryOrder
)

class OrderAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">shopping_cart</i>'
admin.site.register(Order, OrderAdmin)

class RatingAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">rate_review</i>'
admin.site.register(Rating, RatingAdmin)

class DeliveryOrderAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">local_shipping</i>'
admin.site.register(DeliveryOrder, DeliveryOrderAdmin)
