# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import generics

from .models import (
    AppPolicy, FAQCategory, FAQItem,
    State, City
)
from .serializers import (
    AppPolicySerializer, FAQCategorySerializer, 
    FAQItemSerializer, StateSerializer, CitySerializer
)

class AppPolicyDetail(generics.RetrieveAPIView):
    serializer_class = AppPolicySerializer


