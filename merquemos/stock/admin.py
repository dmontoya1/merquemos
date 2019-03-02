# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

from django.contrib import admin

from users.models import User
from .models import (
    Store, StoreContact, StoreHour,
    StoreParameter, Category, Brand,
    BrandStore, Product, Inventory
)


class StoreParameterInline(admin.StackedInline):
    model = StoreParameter
    extra = 0


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">store</i>'
    readonly_fields = ('slug', )
    inlines = [
        StoreParameterInline,
    ]

    manager_readonly_fields = ('name', 'legal_id_number', 'manager', 'slug', 'is_active', )

    def get_queryset(self, request):
        """
        Función para reemplazar el queryset por defecto de django
        si el request.user es un Administrador, entonces solo muestra la tienda
        de ese administrador
        """
        query = super(StoreAdmin, self).get_queryset(request)
        if request.user.user_type == User.MANAGER:
            if request.user.related_store:
                return query.filter(manager=request.user)
        else:
            return query.all()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "manager":
            if request.user.user_type != User.MANAGER:
                kwargs["queryset"] = User.objects.filter(user_type=User.MANAGER)
        return super(StoreAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if request.user.user_type == User.MANAGER:
            return self.manager_readonly_fields
        else:
            return super(StoreAdmin, self).get_readonly_fields(request, obj=obj)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">layers</i>'
    list_display = ('name', 'parent')
    readonly_fields = ('slug', )


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">bookmark</i>'


@admin.register(BrandStore)
class BrandStoreAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">book</i>'
    list_display = ('brand', 'store')


class InventoryInline(admin.StackedInline):
    model = Inventory
    extra = 0
    readonly_fields = ('date_added', 'user')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">storage</i>'
    list_display = ('sku', 'name', 'brand', 'store', 'category', 'price', 'pum_value', 'pum_type', 'tax_percentage', 'size', 'stock_quantity')
    search_fields = ('sku', 'name',)
    readonly_fields = ('stock_quantity', 'slug')
    list_filter = ('store', 'category')
    inlines = [
        InventoryInline,
    ]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.user = request.user
            instance.save(raw=True)
        formset.save()
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(ProductAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['category'].queryset = Category.objects.exclude(parent=None)
        return form


