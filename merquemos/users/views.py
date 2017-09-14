# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework import generics
from rest_framework.response import Response

from .serializers import AddressSerializer
from .models import Address

class AddressList(generics.ListAPIView):
    """Obtiene las direcciones de un usuario, obtenida con base en el token de autenticación de dicho usuario.
    """

    serializer_class = AddressSerializer

    def get(self, request, format=None):
        addresses = Address.objects.filter(user=request.auth.user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

class AddressDetail(generics.RetrieveUpdateDestroyAPIView):
    """Edita (HTTP UPDATE) o elimina (DELETE) la dirección asociada al
    id entregado en la URL
    """

    queryset = Address.objects.all()
    serializer_class = AddressSerializer