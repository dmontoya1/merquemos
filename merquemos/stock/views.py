# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import generics
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


class StoreList(generics.ListAPIView):
    """Obtiene el listado de tiendas activas de la plataforma
    """

    serializer_class = StoreSerializer
    queryset = Store.objects.all()

class CategoryList(generics.ListAPIView):
    """Obtiene el listado de categorias de producto
    """

    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class ProductList(generics.ListAPIView):
    """Obtiene el listado de productos, filtrados por categoría y
    establecimiento. Dichos filtros se envian como 'category_id' para
    categoría y 'store_id' para establecimiento a través parámetros GET
    """

    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.request.query_params.get('category_id', None)
        store_id = self.request.query_params.get('store_id', None)
        if category_id is not None:
            queryset = queryset.filter(category__pk=category_id)
        if store_id is not None:
            queryset = queryset.filter(store__pk=store_id)
        return queryset


