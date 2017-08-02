from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^api/', include('api.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
