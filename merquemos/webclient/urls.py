from django.conf.urls import url, include
from .views import HomePageView, StoreView, ProductView, AuthView

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name="home"),
    url(r'^auth/$', AuthView.as_view(), name="auth"),
    url(r'^stores/(?P<city>[\w-]+)/(?P<slug>[\w-]+)/$', StoreView.as_view(), name='store'),
    url(r'^stores/(?P<store_city>[\w-]+)/(?P<store_slug>[\w-]+)/products/(?P<slug>[\w-]+)/$', ProductView.as_view(), name='product'),
]
