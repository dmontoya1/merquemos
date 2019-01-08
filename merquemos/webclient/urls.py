from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from .views import (
    HomePageView, StoreView, ProductView, 
    AuthView, PrivacyPolicyView, TermsView, FAQView,
    SearchView, CheckoutView, ProfileView, CategoryView,
    SubCategoryView, ExportOrder
)

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name="home"),
    url(r'^login/$', AuthView.as_view(), name="login"),
    url(r'^faq/$', FAQView.as_view(), name="faq"),
    url(r'^signup/$', AuthView.as_view(), name="signup"),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name="logout"),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^checkout/$', CheckoutView.as_view(), name='checkout'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^stores/(?P<city>[\w-]+)/(?P<slug>[\w-]+)/$', StoreView.as_view(), name='store'),
    url(r'^stores/(?P<store_city>[\w-]+)/(?P<store_slug>[\w-]+)/products/(?P<slug>[\w-]+)/$', CategoryView.as_view(), name='category'),
    url(r'^stores/(?P<store_city>[\w-]+)/(?P<store_slug>[\w-]+)/products/(?P<category_parent_slug>[\w-]+)/(?P<slug>[\w-]+)/subcategory/$', SubCategoryView.as_view(), name='subcategory'),
    url(r'^stores/(?P<store_city>[\w-]+)/(?P<store_slug>[\w-]+)/products/(?P<category_slug>[\w-]+)/(?P<slug>[\w-]+)/$', ProductView.as_view(), name='product'),
    url(r'^policies/terms/$', TermsView.as_view(), name="terms"),
    url(r'^policies/privacy/$', PrivacyPolicyView.as_view(), name="privacy-policy"),
    url(r'^export/$', ExportOrder.as_view(), name="privacy-policy"),
]
