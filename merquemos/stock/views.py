# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import generics
from .models import Store
from .serializers import StoreSerializer

class StoreList(generics.ListAPIView):
    """Obtiene el listado de tiendas activas de la plataforma
    """

    serializer_class = StoreSerializer
    queryset = Store.objects.all()