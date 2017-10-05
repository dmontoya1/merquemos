from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from reports.views import ReportsView 
from webclient.views import centrifugo_auth

urlpatterns = [
    url(r'^', include('webclient.urls', namespace='webclient')),
    url(r'^admin/reports/$', ReportsView.as_view(), name="admin-reports"),
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^auth/registration/', include('rest_auth.registration.urls')),
    url(r'^centrifuge/auth/', centrifugo_auth),
    url(r'^api/', include('api.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = 'webclient.views.custom_403'
handler404 = 'webclient.views.custom_404'
handler500 = 'webclient.views.custom_500'