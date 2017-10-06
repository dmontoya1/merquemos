# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from manager.models import City, AppPolicy
from stock.models import Store, Product, Category
from users.models import User


class AuthView(TemplateView):
    template_name = 'auth/auth.html'

    def post(self, request, *args, **kwargs):
        redirect_url = 'webclient:login'

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            redirect_url = 'webclient:home'
        else:
            messages.add_message(request, messages.WARNING, 'Datos inválidos, reintenta nuevamente.')
        return redirect(redirect_url)

class HomePageView(TemplateView):
    template_name = 'home/store_select.html'

    def post(self, request):
        city = City.objects.get(pk=request.POST['city'])
        request.session['city'] = city.pk
        request.session['city__name'] = city.name
        request.session['state__name'] = city.state.name
        return self.get(request)
    
    def get(self, request, format=None):
        if request.GET.get('change_location', None):
            try:
                del request.session['store']
            except KeyError:
                pass
        else:
            if request.session.get('city', False) and request.session.get('store', False):
                city = City.objects.get(pk=request.session['city'])
                store = Store.objects.get(pk=request.session['store']) 
                return redirect('/stores/{}/{}/'.format(city.name, store.slug))
        return super(HomePageView, self).get(request)

    def get_context_data(self, **kwargs):
        request = self.request
        context = super(HomePageView, self).get_context_data(**kwargs)
        if request.session.get('city', False):
            city = City.objects.get(pk=request.session['city'])
            context['stores'] = Store.objects.filter(city=city)
            context['city'] = city
        return context

class StoreView(DetailView):
    model = Store
    template_name = 'home/store_detail.html'

    def get(self, request, city, slug):
        request.session['store'] = self.get_object().pk
        return super(StoreView, self).get(request)

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

class CategoryView(DetailView):
    model = Product
    template_name = 'home/category_detail.html'

    def get_object(self, queryset=None):
        category = Category.objects.get(name=self.kwargs.get('slug')) 
        return category

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        store_id = self.request.session.get('store', None)
        store = Store.objects.get(pk=store_id)
        context['store'] = store
        return context

class SearchView(ListView):
    template_name = 'home/search_result.html'

    def get_queryset(self):
        store_id = self.request.session.get('store', None)
        store = Store.objects.get(pk=store_id)
        q = Product.objects.filter(
            name__icontains=self.request.GET.get('q', ''),
            store=store
        )
        if self.request.GET.get('category', None):
            q = q.filter(category__pk=self.request.GET['category'])
        return q

class CheckoutView(TemplateView):
    template_name = 'orders/checkout.html'

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        context['order'] = self.request.user.get_current_order()
        return context

class ProfileView(TemplateView):
    template_name = 'user/profile.html'

class PrivacyPolicyView(TemplateView):
    template_name = 'home/policy_detail.html'

    def get_context_data(self, **kwargs):
        policies = AppPolicy.objects.all().last()
        context = super(PrivacyPolicyView, self).get_context_data(**kwargs)
        context['name'] = 'Política de privacidad y tratamiento de datos'
        context['content'] = policies.privacy_policy
        return context

class TermsView(TemplateView):
    template_name = 'home/policy_detail.html'

    def get_context_data(self, **kwargs):
        policies = AppPolicy.objects.all().last()
        context = super(TermsView, self).get_context_data(**kwargs)
        context['name'] = 'Terminos y condiciones'
        context['content'] = policies.terms_and_conditions
        return context

def custom_403(request):
    return render(
        request,
        'webclient/403.html',
        status=None
    )

def custom_404(request):
    return render(
        request,
        'webclient/404.html',
        status=None
    )

def custom_500(request):
    return render(
        request,
        'webclient/404.html',
        status=None
    )
