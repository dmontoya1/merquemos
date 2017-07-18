from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^docs/', include('rest_framework_docs.urls')),
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^manager/', include('manager.urls'))
]
