# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import User, Address


class AddressInline(admin.StackedInline):
    model = Address
    max_num = 1
    min_num = 1

class UserAdmin(admin.ModelAdmin):
    inlines = [
        AddressInline,
    ]
admin.site.register(User, UserAdmin)
