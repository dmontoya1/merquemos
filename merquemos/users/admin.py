# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.models import Group
from .models import User, Address


# admin.site.unregister(Group)

class AddressInline(admin.StackedInline):
    model = Address
    extra = 0


class UserAdmin(admin.ModelAdmin):
    inlines = [
        AddressInline,
    ]
    fieldsets = auth_admin.UserAdmin.fieldsets + (("Datos personales",
                                                   {"fields": (
                                                       "user_type", 'phone_number', 'private_hash',)}),)
    readonly_fields = ('private_hash', )


admin.site.register(User, UserAdmin)
