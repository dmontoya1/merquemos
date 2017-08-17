from django.conf.urls import url, include
from .views import (
    StoreList
)

urlpatterns = [
    url(r'^stores/', StoreList.as_view(), name="stores"),
]