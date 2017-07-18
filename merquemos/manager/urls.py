from django.conf.urls import url, include
from django.contrib import admin
from .views import (
    AppPolicyDetail
)

urlpatterns = [
    url(r'^app-policies/', AppPolicyDetail.as_view(), name="app-policies"),
]