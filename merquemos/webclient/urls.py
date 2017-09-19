from django.conf.urls import url, include
from .views import HomePageView, StoreView

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name="home"),
    url(r'^(?P<slug>[\w-]+)/$', StoreView.as_view(), name='store'),
]
