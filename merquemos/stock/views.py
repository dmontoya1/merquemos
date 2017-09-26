# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from api.paginators import PageLimitPagination
from .models import (
    Store,
    Category,
    Product
)
from .serializers import (
    StoreSerializer,
    CategorySerializer,
    ProductSerializer
)


class RequiredParametersMixin(object):
    """Mixin compatible con ListAPIView. Sobreescribe el método 'list' de la
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
        return super(generics.ListAPIView, self).list(request)

class StoreList(generics.ListAPIView):
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

class StoreDetail(generics.RetrieveAPIView):
    """Obtiene el detalle de una tienda  de la plataforma.
    """

    serializer_class = StoreSerializer
    queryset = Store.objects.all()

class CategoryList(generics.ListAPIView):
    """Obtiene el listado de categorias de producto. Si el parámetro
    'parent_category_id' está presente, se filtrara las categorías por el 
    id de categoría padre brindado.
    """

    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.all().filter(parent=None)
        parent_category_id = self.request.query_params.get('parent_category_id')
        if parent_category_id is not None:
            queryset = Category.objects.all().filter(parent__pk=parent_category_id)
        return queryset

class ProductList(RequiredParametersMixin, generics.ListAPIView):
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
            category = Category.objects.get(pk=category_id)
            queryset = category.get_related_products()
            
        return queryset


