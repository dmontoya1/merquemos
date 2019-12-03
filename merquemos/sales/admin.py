# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.http import HttpResponse

from django_xhtml2pdf.utils import generate_pdf

from users.models import User
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


def tienda(obj):
    try:
        return obj.related_items.first().product.store
    except:
        return "Sin Tienda asociada"


total.short_description = 'Total'
tienda.short_description = 'Tienda'


class RatingAdmin(admin.StackedInline):

    model = Rating
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">shopping_cart</i>'
    list_display = ('pk', 'user', 'status', 'comments', total, tienda)
    list_filter = ('status',)
    readonly_fields = ('total', 'date_added', tienda, )
    search_fields = ['user__email', 'user__username']
    inlines = [
        DeliveryOrderAdmin, ItemInline, RatingAdmin
    ]

    def total(self, obj):
        return int(obj.get_total_with_tax())

    def get_queryset(self, request):
        """
        Función para reemplazar el queryset por defecto de django
        si el request.user es un Coordinador, entonces solo muestra los profesores
        de la institución educativa a la que pertenece
        """
        query = super(OrderAdmin, self).get_queryset(request)
        if request.user.user_type == User.MANAGER:
            user_store = request.user.related_store.first()
            return query.filter(related_items__product__store=user_store).distinct()
        else:
            return query.all()

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
