from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import password_reset_confirm
from allauth.account.views import ConfirmEmailView

urlpatterns = [
    url(r'^docs/', include('rest_framework_docs.urls')),
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^manager/', include('manager.urls')),
    url(r'^stock/', include('stock.urls')),
    url(r'^sales/', include('sales.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(), name='account_confirm_email'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, name='password_reset_confirm'),
]
