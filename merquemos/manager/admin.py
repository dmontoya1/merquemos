# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import (
    AppPolicy, FAQCategory, FAQItem, 
    State, City
)

admin.site.register(AppPolicy)
admin.site.register(FAQCategory)
admin.site.register(FAQItem)
admin.site.register(State)
admin.site.register(City)