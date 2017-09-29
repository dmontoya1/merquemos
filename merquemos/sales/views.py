# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from fcm_django.models import FCMDevice

from users.models import Address
from .models import Order, Item, DeliveryOrder
from .serializers import (
    OrderSerializer, OrderItemSerializer, 
    ItemSerializer, OrderHistorySerializer,
    RatingSerializer, OrderDetailSerializer
)


class CurrentOrderDetail(generics.ListAPIView):
    """Obtiene la información de la orden actual del usuario, obtenida con base en el token del usuario.
    Los estados de orden son los siguientes:
        ('PE', 'Pending'),
        ('AC', 'Accepted'),
        ('CA', 'Canceled'),
        ('DE', 'Delivered')
    Si el parámetro 'base_order' está presente, se creará una orden nueva con base a la orden con la llave primaria
    correspondiente al valor de 'base_order'. En éste último escenario, solo se crearán items cuando cada producto tenga
    stock disponible.
    """

    serializer_class = OrderSerializer

    def get(self, request, format=None):
        base_order = None
        if request.GET.get('base_order', None):
            base_order = Order.objects.get(pk=request.GET['base_order'])
            Order.objects.filter(user=request.auth.user, status='PE').delete()
            order = Order(
                user=request.auth.user
            )
            order.save()
            for item in base_order.get_items():
                if item.product.stock_quantity > 0:
                    new_item = Item(
                        product=item.product,
                        order=order,
                        quantity=item.quantity
                    )
                    new_item.save()
        else:
            if Order.objects.filter(user=request.auth.user, status='PE').exists():
                order = Order.objects.get(user=request.auth.user, status='PE')
            else:
                if Order.objects.filter(user=request.auth.user, status='AC').exists():
                    order = Order.objects.get(user=request.auth.user, status='AC')
                else:
                    order = Order(
                        user=request.auth.user
                    )
                    order.save()
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)

class CurrentOrderItems(generics.ListAPIView):
    """Obtiene los items de la orden actual, obtenida con base en el token del usuario.
    """

    serializer_class = OrderItemSerializer

    def get(self, request, format=None):
        if Order.objects.filter(user=request.auth.user, status='PE').exists():
            order = Order.objects.get(user=request.auth.user, status='PE')
        elif Order.objects.filter(user=request.auth.user, status='AC').exists():
            order = Order.objects.get(user=request.auth.user, status='AC')
        else:
            return Response(
                {'detail': 'El usuario no tiene compras activas'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = OrderItemSerializer(order, many=False)
        return Response(serializer.data)

class OrderList(generics.ListAPIView):
    """Obtiene las ordenes de un usuario, obtenido con base en el token de autenticación entregado.
    """

    serializer_class = OrderSerializer

    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.auth.user).exclude(status='PE')
        serializer = OrderHistorySerializer(orders, many=True, context={"request": request})
        return Response(serializer.data)

class OrderDetail(generics.RetrieveDestroyAPIView):
    """Edita (HTTP UPDATE) o elimina (DELETE) la orden asociada al
    id entregado en la URL
    """

    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()

class ItemCreate(generics.CreateAPIView):
    """Crea un nuevo item para una orden.
    """

    serializer_class = ItemSerializer

class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    """Edita (HTTP UPDATE) o elimina (DELETE) el item asociado al
    id entregado en la URL
    """

    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class RatingCreate(generics.CreateAPIView):
    """Crea un nuevo registro de calificación para una orden
    """

    serializer_class = RatingSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        mutable = data._mutable
        data._mutable = True
        data['user'] = request.auth.user.pk
        data._mutable = mutable
        serializer = self.get_serializer(data=data)
        print data
        print serializer
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def checkout(request):
    print request.POST  
    order = Order.objects.get(pk=request.POST['order_id'])
    order.delivery_price = order.get_delivery_price()
    order.status = 'AC'
    order.save()

    address = Address.objects.get(pk=request.POST['address_id'])

    payment_method = request.POST['payment_method']

    delivery_order = DeliveryOrder(
        order=order,
        address=address,
        payment_method=payment_method
    )
    delivery_order.save()

    devices = FCMDevice.objects.filter(user=order.user)

    devices.send_message(
        title="Orden aceptada",
        body="Tu orden está en camino",
        icon="",
        data={
            "order_id": order.pk
        }
    )

    return JsonResponse(
        {
            'detail': 'Compra aceptada satisfactoriamente'
        },
        status=200
    )

@csrf_exempt
def order_cancellation(request):
    order = Order.objects.get(pk=request.POST['order_id'])
    order.status = 'CA'
    order.save()

    return JsonResponse(
        {
            'detail': 'Compra cancelada satisfactoriamente'
        },
        status=200
    )