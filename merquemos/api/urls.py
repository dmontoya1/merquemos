from django.conf.urls import url, include
from django.contrib import admin
from allauth.account.views import ConfirmEmailView

urlpatterns = [
    url(r'^docs/', include('rest_framework_docs.urls')),
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^manager/', include('manager.urls')),
    url(r'^stock/', include('stock.urls')),
    url(r'^sales/', include('sales.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(), name='account_confirm_email'),
]
