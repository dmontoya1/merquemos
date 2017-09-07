from django.conf.urls import url, include
from django.contrib import admin
from .views import (
    OrderDetail, ItemCreate,
    OrderItems, ItemDetail
)

urlpatterns = [
    url(r'^order/$', OrderDetail.as_view(), name="order"),
    url(r'^order/items/$', OrderItems.as_view(), name="order-items"),
    url(r'^item/$', ItemCreate.as_view(), name="item"),
    url(r'^item/(?P<pk>[0-9]+)/$', ItemDetail.as_view(), name="item-detail")
]