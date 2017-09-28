# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView

from manager.models import City
from stock.models import Store, Product
from users.models import User


class AuthView(TemplateView):
    template_name = 'auth/auth.html'

class LoginView(AuthView):

    def post(self, request, *args, **kwargs):
        redirect_url = 'webclient:login'

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            redirect_url = 'webclient:home'
        messages.add_message(request, messages.WARNING, 'Datos inválidos, reintenta nuevamente.')
        return redirect(redirect_url)

class HomePageView(TemplateView):
    template_name = 'home/store_select.html'

class StoreView(DetailView):
    model = Store
    template_name = 'home/store_detail.html'

    def get_object(self, queryset=None):
        try:
            city = City.objects.get(name=self.kwargs.get('city')) 
        except City.DoesNotExist:
            raise Http404("Ups, tienda no encontrada")
        query = self.get_queryset().filter(city=city)
        return super(DetailView, self).get_object(queryset) 

class ProductView(DetailView):
    model = Product
    template_name = 'product/product_detail.html'

    def get_object(self, queryset=None):
        store = Store.objects.get(slug=self.kwargs.get('store_slug')) 
        query = self.get_queryset().filter(store=store)
        return super(DetailView, self).get_object(queryset) 
