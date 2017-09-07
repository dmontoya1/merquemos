from django.conf.urls import url, include
from django.contrib import admin
from .views import (
    OrderDetail, ItemCreate
)

urlpatterns = [
    url(r'^order/', OrderDetail.as_view(), name="order"),
    url(r'^item/', ItemCreate.as_view(), name="item")
]