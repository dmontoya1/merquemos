# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, Address

admin.site.unregister(Group)

class AddressInline(admin.StackedInline):
    model = Address
    extra = 0

class UserAdmin(admin.ModelAdmin):
    inlines = [
        AddressInline,
    ]
    icon = '<i class="material-icons">account_circle</i>'

admin.site.register(User, UserAdmin)
