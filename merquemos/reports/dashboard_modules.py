# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db.models import Avg, Count, Min, Sum, F
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from jet.dashboard.modules import DashboardModule

from manager.models import State, City
from stock.models import Store


class Reports(DashboardModule):

    title = 'Reportes'
    template = 'reports/report_list.html'

    def init_with_context(self, context):
        self.children = Store.objects.all()
        self.states = State.objects.all()
