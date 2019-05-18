from django.conf.urls import url, include

from . import views


app_name = 'reports'
urlpatterns = [
    # url(r'^', views.ReportView.as_view(), name="reports"),
    url(r'^products/', views.RegisteredProducts.as_view(), name='products'),
    url(r'^services/', views.NumberServices.as_view(), name='services'),
    url(r'^rating/', views.Rating.as_view(), name='rating'),
    url(r'^sales/', views.Sales.as_view(), name='sales'),
    url(r'^requests/', views.Requests.as_view(), name='requests'),
    
]