from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from .views import HomePageView, StoreView, ProductView, LoginView 

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name="home"),
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^signup/$', LoginView.as_view(), name="signup"),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name="logout"),
    url(r'^stores/(?P<city>[\w-]+)/(?P<slug>[\w-]+)/$', StoreView.as_view(), name='store'),
    url(r'^stores/(?P<store_city>[\w-]+)/(?P<store_slug>[\w-]+)/products/(?P<slug>[\w-]+)/$', ProductView.as_view(), name='product'),
]
