# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import (
    AppPolicy, FAQCategory,  
    State, City
)

class AppPolicyAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">security</i>'
admin.site.register(AppPolicy, AppPolicyAdmin)

class FAQCategoryAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">assistant_photo</i>'
admin.site.register(FAQCategory, FAQCategoryAdmin)

class StateAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">map</i>'
admin.site.register(State, StateAdmin)

class CityAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">place</i>'
admin.site.register(City, CityAdmin)

