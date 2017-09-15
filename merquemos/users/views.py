# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import AddressSerializer, AddressCreateSerializer
from .models import Address

class AddressCreate(generics.CreateAPIView):
    """Crea una dirección, asignada al usuario del token de autenticación enviado
    """

    serializer_class = AddressCreateSerializer

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.auth.user
        serializer = self.get_serializer(data=request.data)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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