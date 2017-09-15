from django.conf.urls import url, include
from .views import (
    AddressList, AddressDetail, AddressCreate
)

urlpatterns = [
    url(r'^address/$', AddressCreate.as_view(), name="address-create"),
    url(r'^addresses/$', AddressList.as_view(), name="addresses"),
    url(r'^addresses/(?P<pk>[0-9]+)/$', AddressDetail.as_view(), name="address-detail")
]