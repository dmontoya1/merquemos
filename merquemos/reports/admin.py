# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import ProductSummary


@admin.register(ProductSummary)
class ProductSummaryAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    def changelist_view(self, request, extra_context=None):
        response = super(ProductSummaryAdmin, self).changelist_view(
            request,
            extra_context=extra_context,
        )

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['summary'] = qs
        
        return response
