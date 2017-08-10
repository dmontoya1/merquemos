# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class AuthTokenConfig(AppConfig):
    name = 'rest_framework.authtoken'
    verbose_name = "Tokens de autenticación"
