# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView

class ReportsView(TemplateView):
    template_name = "reports_index.html"