from django.conf.urls import url, include
from .views import (
    StoreList,
    CategoryList,
    CategoryDetail,
    ProductList,
    StoreDetail,
    ProductDetail,
    BrandList,
    BrandStoreList,
    InventoryList,
    BrandDetail,
    BrandStoreDetail
)

urlpatterns = [
    url(r'^stores/', StoreList.as_view(), name="stores"),
    url(r'^store/(?P<pk>[0-9]+)/$', StoreDetail.as_view(), name="store-detail"),
    url(r'^categories/$', CategoryList.as_view(), name="categories"),
    url(r'^categories/(?P<pk>\d+)/', CategoryDetail.as_view(), name="categorie"),
    url(r'^products/$', ProductList.as_view(), name="products"),
    url(r'^products/(?P<pk>\d+)/', ProductDetail.as_view(), name="product"),
    url(r'^inventory/$', InventoryList.as_view(), name="inventory"),   
    url(r'^brands/$', BrandList.as_view(), name="brands"),
    url(r'^brands/(?P<pk>\d+)/', BrandDetail.as_view(), name="brand"),
    url(r'^store-brands/$', BrandStoreList.as_view(), name="store-brands"),
    url(r'^store-brands/(?P<pk>\d+)/', BrandStoreDetail.as_view(), name="store-brand"),
]