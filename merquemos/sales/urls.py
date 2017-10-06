from django.conf.urls import url, include
from django.contrib import admin
from .views import (
    CurrentOrderDetail, ItemCreate, OrderList,
    CurrentOrderItems, ItemDetail, OrderDetail, checkout,
    RatingCreate, order_cancellation
)

urlpatterns = [
    url(r'^current-order/$', CurrentOrderDetail.as_view(), name="current-order"),
    url(r'^current-order/items/$', CurrentOrderItems.as_view(), name="current-order-items"),
    url(r'^orders/$', OrderList.as_view(), name="order-list"),
    url(r'^order/(?P<pk>[0-9]+)/$', OrderDetail.as_view(), name="order-detail"),
    url(r'^item/$', ItemCreate.as_view(), name="item-create"),
    url(r'^item/(?P<pk>[0-9]+)/$', ItemDetail.as_view(), name="item-detail"),
    url(r'^checkout/$', checkout, name="checkout"),
    url(r'^cancellation/$', order_cancellation, name="cancellation"),
    url(r'^rating/$', RatingCreate.as_view(), name="rating-create"),
]