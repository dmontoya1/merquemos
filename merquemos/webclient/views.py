# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView

from stock.models import Store

class HomePageView(TemplateView):
    template_name = 'home/store_select.html'

class StoreView(DetailView):
    model = Store
    template_name = 'home/store_detail.html'