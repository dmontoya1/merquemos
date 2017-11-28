from django.conf.urls import url, include
from django.contrib import admin
from .views import (
    AppPolicyDetail, FAQCategoryList, FAQItemList, CityDetail,
    StateList, StateDetail, CityList, ContactMessageCreate
)

urlpatterns = [
    url(r'^app-policies/', AppPolicyDetail.as_view(), name="app-policies"),
    url(r'^faq-categories/', FAQCategoryList.as_view(), name="faq-categories"),
    url(r'^faq-items/', FAQItemList.as_view(), name="faq-items"),
    url(r'^states/$', StateList.as_view(), name="states"),
    url(r'^states/(?P<pk>\d+)/', StateDetail.as_view(), name="state"),
    url(r'^cities/$', CityList.as_view(), name="cities"),
    url(r'^cities/(?P<pk>\d+)/', CityDetail.as_view(), name="city"),
    url(r'^contact/', ContactMessageCreate.as_view(), name="contact"),
]