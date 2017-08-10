# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import (
    Store, StoreContact, StoreHour,
    StoreParameter, Category, Brand,
    BrandStore, Product, Inventory
)


class StoreAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">store</i>'
admin.site.register(Store, StoreAdmin)

class CategoryAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">layers</i>'
admin.site.register(Category, CategoryAdmin)

class BrandAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">bookmark</i>'
admin.site.register(Brand, BrandAdmin)

class BrandStoreAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">book</i>'
    list_display = ('brand', 'store')
admin.site.register(BrandStore, BrandStoreAdmin)

class InventoryInline(admin.StackedInline):
    model = Inventory
    extra = 0
    readonly_fields = ('date_added', 'user')

class ProductAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">storage</i>'
    list_display = ('code', 'name', 'brand', 'store', 'category', 'price', 'tax_percentage', 'size', 'stock_quantity')
    readonly_fields = ('stock_quantity',)
    inlines = [
        InventoryInline,
    ]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.user = request.user
            instance.save()
        formset.save()
admin.site.register(Product, ProductAdmin)

