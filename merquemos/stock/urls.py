from django.conf.urls import url, include
from .views import (
    StoreList,
    CategoryList,
    ProductList
)

urlpatterns = [
    url(r'^stores/', StoreList.as_view(), name="stores"),
    url(r'^categories/', CategoryList.as_view(), name="categories"),
    url(r'^products/', ProductList.as_view(), name="products"),
]