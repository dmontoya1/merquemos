# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import xlwt

from django.db.models import Avg, Count, Min, Sum, F
from django.http import HttpResponse
from django.shortcuts import render
from django_xhtml2pdf.utils import generate_pdf
from django.views.generic import TemplateView

from manager.models import State, City
from sales.models import Order
from stock.models import Product, Store
# from users.models import User


class ReportView(TemplateView):
    template_name = 'reports/report_list.html'

    def get_context_data(self, **kwargs):
        context = super(ReportView, self).get_context_data(**kwargs)
        context['stores'] = Store.objects.all()
        states = State.objects.all()
        context['states'] = State.objects.all()
        return context
    
    def generate_pdf_report(self, request, report, start_date, end_date):
        if report == "register_products":
            products = Product.objects.filter(date_added__gte=start_date, date_added__lte=end_date)
            context = {
                'headers': (
                    'Nombre',
                    'Descripción',
                    'Precio',
                ),
                'products': products,
                'start_date': start_date,
                'end_date': end_date
            }
            report_template_name = 'reports/products_registered.html'
        elif report == "number_services":
            store = Store.objects.get(pk=request.POST['store'])
            orders = Order.objects.filter(
                related_items__product__store=store, 
                status='DE', 
                date_added__gte=start_date, 
                date_added__lte=end_date
            )
            orders_count = orders.count()
            total_no_tax = 0
            total_tax = 0
            total_with_tax = 0
            if orders_count > 0:
                for order in orders:
                    total_no_tax += order.get_total_no_tax()
                    total_tax += order.get_total_tax()
                    total_with_tax += order.get_total_with_tax()

            context = {
                'store': store,
                'count': orders_count,
                'start_date': start_date,
                'end_date': end_date,
                'total_no_tax': total_no_tax,
                'total_tax': total_tax,
                'total_with_tax': total_with_tax
            }
            report_template_name = 'reports/number_services.html'
        elif report == "rating":
            orders = Order.objects.filter(date_added__gte=start_date, date_added__lte=end_date)

            context = {
                'headers': (
                    'Establecimiento',
                    '# Orden', 
                    'Fecha', 
                    'Calificación',
                    'Nombre de usuario',
                    'Correo',
                    'Teléfono'
                ),
                'orders': orders
            }
            report_template_name = 'reports/ratings.html'
        elif report == "sales":
            city = City.objects.get(pk=request.POST['city'])
            store = Store.objects.get(pk=request.POST['store'])
            orders = Order.objects.filter(
                related_items__product__store=store,
                date_added__gte=start_date, 
                date_added__lte=end_date,
                city=city,
                status='DE'
            )
             
            context = {
                'headers': (
                    'Establecimiento',
                    '# Orden', 
                    'Fecha', 
                    'Estado',
                    'Precio total',
                    'Valor Domicilio'
                ),
                'orders': orders,
                'store': store,
                'start_date':start_date,
                'end_date': end_date
            }
            report_template_name = 'reports/sales.html'
        elif report == "requests":
            city = City.objects.get(pk=request.POST['city'])
            store = Store.objects.get(pk=request.POST['store'])
            orders = Order.objects.filter(
                related_items__product__store=store,
                date_added__gte=start_date, 
                date_added__lte=end_date,
            )

            context = {
                'headers': (
                    'Establecimiento',
                    '# Orden', 
                    'Fecha', 
                    'Estado',
                    'Precio total',
                    'Nombre usuario',
                    'Correo'
                ),
                'orders': orders,
                'store': store,
                'start_date':start_date,
                'end_date': end_date
            }
            report_template_name = 'reports/requests.html'
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'
        result = generate_pdf(report_template_name, file_object=response, context=context)
        return response
    
    def post(self, request, *args, **kwargs):
        report = request.POST['report']
        start_date = request.POST['start']
        end_date = request.POST['end']
        return self.generate_pdf_report(request, report, start_date, end_date)
