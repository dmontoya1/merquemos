# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import xlwt

from django.http import HttpResponse
from django.shortcuts import render
from django_xhtml2pdf.utils import generate_pdf
from django.views.generic import TemplateView

from stock.models import Product
# from users.models import User


class ReportView(TemplateView):
    template_name = 'reports/report_list.html'

    # def get_context_data(self, **kwargs):
    #     context = super(ReportView, self).get_context_data(**kwargs)
    #     if self.request.user.user_type != self.request.user.COORDINADOR:
    #         context['schools'] = School.objects.all()
    #     else:
    #         context['students'] = Student.objects.filter(school=self.request.user.school)
    #     return context
    
    def generate_pdf_report(self, request, report):
        if report == "route_record":
            student = Student.objects.get(pk=request.POST['student'])
            context = {
                'headers': (
                    'Fecha',
                    'Ruta',
                    'Conductor',
                    'Estado',
                    'Hora subida',
                    'Hora bajada',
                    'Lat subida',
                    'Long subida',
                    'Lat bajada',
                    'Long bajada'
                ),
                'student': student,
                'route_records': RouteRecord.objects.filter(student=student)
            }
            report_template_name = 'reports/route_record.html'
        elif report == "routes":  
            context = {
                'headers': ('Nombre',  'Conductor', 'Tipo ID Conductor', 'Num ID conductor', 'Celular conductor', 'Estudiantes'),
                'routes': Route.objects.filter(school=request.user.school),
                'school': request.user.school
            }
            report_template_name = 'reports/routes.html'
        elif report == "daily_routes":
            context = {
                'headers': ('Nombre',  'Conductor', 'Registros de ruta'),
                'routes': Route.objects.filter(school=request.user.school),
                'school': request.user.school
            }
            report_template_name = 'reports/daily_route.html'
        elif report == "no_attendance":
            context = {
                'headers': (
                    'Fecha',
                    'Estudiante', 
                    'Ruta', 
                    'Comentarios'
                ),
                'records': RouteRecord.objects.filter(route__school=request.user.school, status='NA')
            }
            report_template_name = 'reports/no_attendance.html'
        elif report == "max_managers":
            if self.request.user.user_type != self.request.user.COORDINADOR:
                school = request.POST['school']
            else:
                school = request.user.school
            context = {
                'headers': (
                    'Nombre',
                    'Tipo documento', 
                    '# documento', 
                    'Calendario',
                    'Grado',
                    'Acudientes'
                ),
                'records': Student.objects.filter(school=school, related_student_manager__status='AP').distinct()
            }
            report_template_name = 'reports/max_managers.html'
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'
        result = generate_pdf(report_template_name, file_object=response, context=context)
        return response
    
    def generate_xlsx_report(self, request, report):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="reporte.xls"'
        
        wb = xlwt.Workbook(encoding='utf-8')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        if report == "route_record":
            student = Student.objects.get(pk=request.POST['student'])
            records = RouteRecord.objects.filter(student=student).values_list(
                'date',
                'route__name',
                'route__driver__document_id',
                'status',
                'boarding_time',
                'landing_time',
                'boarding_latitude',
                'boarding_longitude',
                'landing_latitude',
                'landing_longitude'
            )

            ws = wb.add_sheet(str(student))

            columns = [
                'Fecha',
                'Ruta',
                'Conductor',
                'Estado',
                'Hora subida',
                'Hora bajada',
                'Lat subida',
                'Long subida',
                'Lat bajada',
                'Long bajada'
            ]

        elif report == "routes":  
            records = Route.objects.filter(school=request.user.school).values_list(
                'name',
                'driver__name',
                'driver__document_type',
                'driver__document_id',
                'driver__cellphone'
            )

            ws = wb.add_sheet('Rutas')

            columns = [
                'Nombre',
                'Conductor',
                'Tipo ID Conductor',
                'Num ID conductor',
                'Celular conductor'
            ]
        elif report == "daily_routes":
            records = Route.objects.filter(school=request.user.school).values_list(
                'name',
                'driver__name',
                'driver__document_type'
            )

            ws = wb.add_sheet('Rutas diarias')

            columns = [
                'Nombre',
                'Nombre conductor',
                'Num ID conductor'
            ]
        elif report == "no_attendance":
            records = RouteRecord.objects.filter(route__school=request.user.school, status='NA').values_list(
                'date',
                'student',
                'route',
                'comments'
            )

            ws = wb.add_sheet('Inasistencias')

            columns = [
                'Fecha',
                'Estudiante',
                'Ruta',
                'comentarios'
            ]
        elif report == "max_managers":
            if self.request.user.user_type != self.request.user.COORDINADOR:
                school = request.POST['school']
            else:
                school = request.user.school
            records = Student.objects.filter(school=school, related_student_manager__status='AP').distinct().values_list(
                'first_name',
                'document_type',
                'document_id',
                'calendar',
                'level'
            )

            ws = wb.add_sheet('Estudiantes con 3 acudientes')

            columns = [
                'Nombre',
                'Tipo documento', 
                '# documento', 
                'Calendario',
                'Grado'
            ]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()

        for row in records:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)

        return response

    def post(self, request, *args, **kwargs):
        report = request.POST['report']
        report_type = request.POST['report_type']
        if report_type == "pdf":
            return self.generate_pdf_report(request, report)
        else:
            return self.generate_xlsx_report(request, report)
