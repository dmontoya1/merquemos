# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from .models import Order, Item
from .serializers import OrderSerializer, OrderItemSerializer, ItemSerializer

class OrderDetail(generics.ListAPIView):
    """Obtiene la información de la orden actual del usuario, obtenida con base en el token del usuario.
    """

    serializer_class = OrderSerializer

    def get(self, request, format=None):
        order = Order.objects.filter(user=request.auth.user, status='PE').exists()
        if order:
            order = Order.objects.get(user=request.auth.user, status='PE')
        else:
            order = Order(
                user=request.auth.user
            )
            order.save()
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)

class OrderItems(generics.ListAPIView):
    """Obtiene los items de la orden actual, obtenida con base en el token del usuario.
    """

    serializer_class = OrderItemSerializer

    def get(self, request, format=None):
        order = Order.objects.filter(user=request.auth.user, status='PE').exists()
        if order:
            order = Order.objects.get(user=request.auth.user, status='PE')
        else:
            return Response(
                {'detail': 'El usuario no tiene compras activas'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = OrderItemSerializer(order, many=False)
        return Response(serializer.data)

class ItemCreate(generics.CreateAPIView):
    """Crea un nuevo item para una orden.
    """

    serializer_class = ItemSerializer
    


