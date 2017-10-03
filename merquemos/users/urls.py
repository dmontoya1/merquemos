from django.conf.urls import url, include
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from .views import (
    AddressList, AddressDetail, AddressCreate
)
from .views import FacebookAuth, GoogleAuth

urlpatterns = [
    url(r'^address/$', AddressCreate.as_view(), name="address-create"),
    url(r'^addresses/$', AddressList.as_view(), name="addresses"),
    url(r'^addresses/(?P<pk>[0-9]+)/$', AddressDetail.as_view(), name="address-detail"),
    url(r'^devices/$', FCMDeviceAuthorizedViewSet.as_view({'post': 'create'}), name='create_fcm_device'),
    url(r'^test-push/$', FCMDeviceAuthorizedViewSet.as_view({'post': 'create'}), name='test_fcm_device'),
    url(r'^auth/facebook/$', FacebookAuth.as_view(), name='fb_login'),
    url(r'^auth/google/$', GoogleAuth.as_view(), name='gl_login')
]