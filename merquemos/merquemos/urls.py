from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from reports.views import ReportView 

urlpatterns = [
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^admin/', admin.site.urls),
    url(r'^admin/reports/$', ReportView.as_view(), name="admin-reports"),
    url(r'^', include('webclient.urls', namespace='webclient')),
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^reports/', include('reports.urls', namespace='reports')),
    url(r'^auth/registration/', include('rest_auth.registration.urls')),
    url(r'^api/', include('api.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'webclient.views.custom_404'

admin.site.site_header = 'Administrador Mequemos'
admin.site.site_title = 'Administrador Mequemos'