from django.conf.urls import url, include
from .views import (
    StoreList,
    CategoryList,
    ProductList,
    StoreDetail,
    ProductDetail
)

urlpatterns = [
    url(r'^stores/', StoreList.as_view(), name="stores"),
    url(r'^store/(?P<pk>[0-9]+)/$', StoreDetail.as_view(), name="store-detail"),
    url(r'^categories/', CategoryList.as_view(), name="categories"),
    url(r'^products/$', ProductList.as_view(), name="products"),
    url(r'^products/(?P<pk>\d+)/', ProductDetail.as_view(), name="product"),
]