# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response

from .models import (
    AppPolicy, FAQCategory, FAQItem,
    State, City
)
from .serializers import (
    AppPolicySerializer, FAQCategorySerializer, ContactMessageSerializer,
    FAQItemSerializer, StateSerializer, CitySerializer
)


class AppPolicyDetail(generics.ListAPIView):
    """Obtiene las polizas de usuario de la aplicación.
    
    Cada poliza es un campo de la tabla.
    """

    serializer_class = AppPolicySerializer

    def get(self, request, format=None):
        app_policies = AppPolicy.objects.all().last()
        if app_policies:
            serializer = AppPolicySerializer(app_policies, many=False)
        return Response(serializer.data)

class FAQCategoryList(generics.ListAPIView):
    """Obtiene las categorías de preguntas frecuentes.
    """

    serializer_class = FAQCategorySerializer
    queryset = FAQCategory.objects.all()

class FAQItemList(generics.ListAPIView):
    """Obtiene los item de preguntas frecuentes, filtrados por categoría mediante
    el parámetro 'faqcategory_id'.
    """

    serializer_class = FAQItemSerializer

    def get_queryset(self):
        queryset = FAQItem.objects.all()
        faqcategory_id = self.request.query_params.get('faqcategory_id', None)
        if faqcategory_id is not None:
            queryset = queryset.filter(category__pk=faqcategory_id)
        return queryset

class StateList(generics.ListCreateAPIView):
    """Obtiene y crea los departamentos (regiones).
    """
    
    serializer_class = StateSerializer

    def get_queryset(self):
        queryset = State.objects.all()

        return queryset

class StateDetail(generics.RetrieveUpdateDestroyAPIView):
    """Obtiene y edita un departamento (region).
    """
    
    serializer_class = StateSerializer
    queryset = State.objects.all()

class CityList(generics.ListCreateAPIView):
    """Obtiene y crea los municipios (ciudades), filtrados por departamento mediante
    el parámetro 'state_id'.
    """
    
    serializer_class = CitySerializer

    def get_queryset(self):
        queryset = City.objects.all()
        state_id = self.request.query_params.get('state_id', None)
        if state_id is not None:
            queryset = queryset.filter(state__pk=state_id)
        
        return queryset

class CityDetail(generics.RetrieveUpdateDestroyAPIView):
    """Obtiene y edita un municipio (ciudad).
    """
    
    serializer_class = CitySerializer
    queryset = City.objects.all()

class ContactMessageCreate(generics.CreateAPIView):
    """Crea un nuevo registro de contacto
    """

    serializer_class = ContactMessageSerializer