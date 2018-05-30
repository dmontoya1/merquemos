# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from api.paginators import PageLimitPagination
from .models import (
    Store,
    Category,
    Product, 
    Brand,
    BrandStore
)
from .serializers import (
    StoreSerializer,
    CategorySerializer,
    ProductSerializer,
    BrandSerializer,
    BrandStoreSerializer
)


class RequiredParametersMixin(object):
    """Mixin compatible con ListCreateAPIView. Sobreescribe el método 'list' de la
    clase para añadir un filtrado de parámetros requeridos en el request.
    """
    required_parameters = []

    def list(self, request):
        detail = 'El parametro \'{}\' es requerido'
        for parameter in self.required_parameters:
            if not request.query_params.get(parameter, None):
                return Response({
                    'detail': detail.format(parameter)
                }, status.HTTP_400_BAD_REQUEST)
        return super(generics.ListCreateAPIView, self).list(request)

class StoreList(generics.ListCreateAPIView):
    """Obtiene el listado de tiendas activas de la plataforma. Si el parámetro 
    'city_id' está presente, se filtrarán las tiendas por el id de la ciudad brindada.
    """

    serializer_class = StoreSerializer

    def get_queryset(self):
        queryset = Store.objects.all()
        city_id = self.request.query_params.get('city_id')
        if city_id:
            queryset = queryset.filter(city__pk=city_id)
        return queryset

class StoreDetail(generics.RetrieveUpdateDestroyAPIView):
    """Obtiene el detalle de una tienda  de la plataforma.
    """

    serializer_class = StoreSerializer
    queryset = Store.objects.all()

class CategoryList(RequiredParametersMixin, generics.ListCreateAPIView):
    """Obtiene el listado de categorias de producto, filtrados por tienda
    obtenida desde el parámetro GET 'store_id'. Si el parámetro
    'parent_category_id' está presente, se filtrara las categorías por el 
    id de categoría padre brindado. 
    """

    serializer_class = CategorySerializer
    required_parameters = ['store_id']

    def get_queryset(self):
        queryset = Category.objects.all().filter(parent=None)
        store = Store.objects.get(pk=self.request.query_params.get('store_id'))
        parent_category_id = self.request.query_params.get('parent_category_id')
        if parent_category_id is not None:
            queryset = Category.objects.all().filter(parent__pk=parent_category_id)
        for category in queryset:
            if category.get_related_products(store=store).count() == 0:
                queryset = queryset.exclude(pk=category.pk)
        return queryset

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    """Obtiene el detalle de una categoria.
    """

    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class ProductList(RequiredParametersMixin, generics.ListCreateAPIView):
    """Obtiene el listado de productos, filtrados por categoría y
    establecimiento. Dichos filtros se envian como 'category_id' para
    categoría y 'store_id' para establecimiento a través parámetros GET y son 
    obligatorios. Para la paginación, se requiere el parámetro 'limit' con un
    entero como valor, el cual indicará la cantidad de productos a mostrar por página.
    """

    serializer_class = ProductSerializer
    pagination_class = PageLimitPagination
    required_parameters = ['store_id', 'limit']

    def get_queryset(self):
        queryset = Product.objects.all()
        
        store_id = self.request.query_params.get('store_id')
        queryset = queryset.filter(store__pk=store_id)

        q_term = self.request.query_params.get('q', None)

        if q_term is not None:
            queryset = queryset.filter(name__icontains=q_term)

        category_id = self.request.query_params.get('category_id', None)

        if category_id is not None:
            store = Store.objects.get(pk=store_id)
            category = Category.objects.get(pk=category_id)
            queryset = category.get_related_products(store=store)

        return queryset

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    """Obtiene el detalle de un producto
    """

    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class BrandList(generics.ListCreateAPIView):
    """Obtiene el listado de marcas activas de la plataforma. 
    """

    serializer_class = BrandSerializer
    queryset = Brand.objects.all()

class BrandDetail(generics.RetrieveUpdateDestroyAPIView):
    """Obtiene el detalle de una marca 
    """

    serializer_class = BrandSerializer
    queryset = Brand.objects.all()

class BrandStoreList(generics.ListCreateAPIView):
    """Obtiene el listado de marcas activas de la plataforma por tienda. Filtrado opcionalmente por store_id
    """

    serializer_class = BrandStoreSerializer

    def get_queryset(self):
        queryset = BrandStore.objects.all()
        store_id = self.request.query_params.get('store_id')
        if store_id:
            queryset = queryset.filter(store__pk=store_id)
        return queryset

class BrandStoreDetail(generics.RetrieveUpdateDestroyAPIView):
    """Obtiene el detalle de una marca por tienda.
    """

    serializer_class = BrandStoreSerializer
    queryset = BrandStore.objects.all()

