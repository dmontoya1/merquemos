# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import (
    Order, Item, Rating,
    DeliveryOrder
)


class ItemInline(admin.TabularInline):
    model = Item
    readonly_fields = ('product', 'quantity', 'tax_percentage', 'price', 'total')
    list_display = ('store', 'product', 'brand', 'quantity', 'tax_percentage', 'price', 'total')
    extra = 0

    def store(self, instance):
        return str(instance.product.store.name)

    def brand(self, instance):
        return str(instance.product.brand.name)

    store.short_description = "Tienda"
    brand.short_description = "Marca"

def total(obj):
    return obj.get_total_with_tax()
total.short_description = 'Total'

class OrderAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">shopping_cart</i>'
    list_display = ('pk', 'user', 'status', 'comments', 'total')
    list_filter = ('status',)
    search_fields = ['user__email', 'user__username']
    inlines = [
        ItemInline,
    ]

    

admin.site.register(Order, OrderAdmin)


class RatingAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">rate_review</i>'
admin.site.register(Rating, RatingAdmin)


class DeliveryOrderAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">local_shipping</i>'
admin.site.register(DeliveryOrder, DeliveryOrderAdmin)
