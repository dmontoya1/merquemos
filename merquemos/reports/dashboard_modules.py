# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db.models import Avg, Count, Min, Sum, F
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from jet.dashboard.modules import DashboardModule


class ReportView(DashboardModule):

    title = 'Reportes'
    template_name = 'reports/report_list.html'
