from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^api/', include('api.urls'))
]
