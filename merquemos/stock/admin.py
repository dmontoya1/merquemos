# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import (
    Store, StoreContact, StoreHour,
    StoreParameter, Category, Brand,
    BrandStore, Product, Inventory
)

admin.site.register(Store)
admin.site.register(StoreContact)
admin.site.register(StoreHour)
admin.site.register(StoreParameter)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(BrandStore)
admin.site.register(Product)
admin.site.register(Inventory)

