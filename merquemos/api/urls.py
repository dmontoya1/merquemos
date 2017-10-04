from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import (
    password_reset, password_reset_done,
    password_reset_confirm, password_reset_complete
)
from allauth.account.views import ConfirmEmailView


urlpatterns = [
    url(r'^docs/', include('rest_framework_docs.urls')),
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^manager/', include('manager.urls')),
    url(r'^stock/', include('stock.urls')),
    url(r'^sales/', include('sales.urls', namespace='sales')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(), name='account_confirm_email'),
    url(
        regex=r'^contrib/password_reset/$',
        view=password_reset,
        name='password_reset'
    ),
    url(
        regex=r'^contrib/password_reset/done/$',
        view=password_reset_done,
        name='password_reset_done'
    ),
    url(
        regex=r'^contrib/reset/(?P<uidb64>[0-9A-Za-z_\-]+)'
              r'/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        view=password_reset_confirm,
        name='password_reset_confirm'
    ),
    url(
        regex=r'^contrib/reset/done/$',
        view=password_reset_complete,
        name='password_reset_complete'
    ),
]
