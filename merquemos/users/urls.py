from django.conf.urls import url, include
from .views import (
    AddressList
)

urlpatterns = [
    url(r'^addresses/', AddressList.as_view(), name="addresses")
]