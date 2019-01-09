from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html

from django_xhtml2pdf.utils import generate_pdf
