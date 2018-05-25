from django.conf.urls import url, include
from .views import (
    StoreList,
    CategoryList,
    ProductList,
    StoreDetail,
    ProductDetail,
    BrandList,
    BrandStoreList,
    InventoryList
)

urlpatterns = [
    url(r'^stores/', StoreList.as_view(), name="stores"),
    url(r'^brands/', BrandList.as_view(), name="brands"),
    url(r'^store-brands/', BrandStoreList.as_view(), name="store-brands"),
    url(r'^store/(?P<pk>[0-9]+)/$', StoreDetail.as_view(), name="store-detail"),
    url(r'^categories/', CategoryList.as_view(), name="categories"),
    url(r'^products/$', ProductList.as_view(), name="products"),
    url(r'^inventory/$', InventoryList.as_view(), name="inventory"),
    url(r'^products/(?P<pk>\d+)/', ProductDetail.as_view(), name="product"),
]