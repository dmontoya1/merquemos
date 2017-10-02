# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import AddressSerializer, AddressCreateSerializer
from .models import Address


class AddressCreate(generics.CreateAPIView):
    """Crea una dirección, asignada al usuario del token de autenticación enviado
    """

    serializer_class = AddressCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.auth.user)

class AddressList(generics.ListAPIView):
    """Obtiene las direcciones de un usuario, obtenida con base en el token de autenticación de dicho usuario.
    Si el parámetro 'state_id' está presente, se filtrarán las direcciones por el departamento con el id correspondiente.
    """

    serializer_class = AddressSerializer

    def get(self, request, format=None):
        addresses = Address.objects.filter(user=request.auth.user)
        print request.auth.user.pk
        state_id = self.request.query_params.get('state_id', None)
        if state_id is not None:
            addresses = addresses.filter(city__state__pk=state_id)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

class AddressDetail(generics.RetrieveUpdateDestroyAPIView):
    """Edita (HTTP UPDATE) o elimina (DELETE) la dirección asociada al
    id entregado en la URL
    """

    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class SocialAuth(APIView):
    """
    Administra el registro/login con redes sociales

    * No requiere token de autenticación
    """

    def post(self, request):
        print request
        email = request.POST['email']
        return Response({"detail": "Error accessing FB user profile."}, status=400)