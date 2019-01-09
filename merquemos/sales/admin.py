# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.http import HttpResponse

from django_xhtml2pdf.utils import generate_pdf

from .models import (
    Order, Item, Rating,
    DeliveryOrder
)


class DeliveryOrderAdmin(admin.StackedInline):

    model = DeliveryOrder
    readonly_fields = ('address', )
    extra = 0

    def has_add_permission(self, obj):
        return False


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
    return int(obj.get_total_with_tax())

total.short_description = 'Total'


class OrderAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">shopping_cart</i>'
    list_display = ('pk', 'user', 'status', 'comments', total,)
    list_filter = ('status',)
    readonly_fields = ('total', 'date_added')
    search_fields = ['user__email', 'user__username']
    inlines = [
        DeliveryOrderAdmin, ItemInline, 
    ]

    def total(self, obj):
        return int(obj.get_total_with_tax())

    def response_change(self, request, obj):
        """
        """

        opts = self.model._meta
        custom_redirect = False

        if "export-invoice" in request.POST:
            context = {
                'order': obj,
            }
            report_template_name = 'admin/order_resume.html'
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="factura.pdf"'
            result = generate_pdf(report_template_name, file_object=response, context=context)
            return response
        return super(OrderAdmin, self).response_change(request, obj)

admin.site.register(Order, OrderAdmin)



class RatingAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">rate_review</i>'
admin.site.register(Rating, RatingAdmin)


