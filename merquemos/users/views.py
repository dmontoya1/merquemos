# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.sites.models import Site
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters

from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from allauth.socialaccount import providers
from allauth.socialaccount.models import SocialLogin, SocialToken, SocialApp
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.helpers import complete_social_login

from rest_auth.registration.views import SocialLoginView
from rest_auth.app_settings import UserDetailsSerializer

from api.helpers import get_api_user
from .serializers import AddressSerializer, AddressCreateSerializer, PasswordChangeSerializer
from .models import Address


class AddressCreate(generics.CreateAPIView):
    """Crea una dirección, asignada al usuario del token de autenticación enviado
    """

    serializer_class = AddressCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=get_api_user(self.request))

class AddressList(generics.ListAPIView):
    """Obtiene las direcciones de un usuario, obtenida con base en el token de autenticación de dicho usuario.
    Si el parámetro 'state_id' está presente, se filtrarán las direcciones por el departamento con el id correspondiente.
    """

    serializer_class = AddressSerializer

    def get(self, request, format=None):
        addresses = Address.objects.filter(user=request.auth.user)
        print request.auth.user.pk
        state_id = self.request.query_params.get('state_id', None)
        if state_id is not None:
            addresses = addresses.filter(city__state__pk=state_id)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

class AddressDetail(generics.RetrieveUpdateDestroyAPIView):
    """Edita (HTTP UPDATE) o elimina (DELETE) la dirección asociada al
    id entregado en la URL
    """

    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class UserDetailsView(generics.RetrieveUpdateAPIView):
    serializer_class = UserDetailsSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        return get_api_user(self.request)

    def get_queryset(self):
        return get_user_model().objects.none()

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)

class PasswordChangeView(generics.GenericAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = (AllowAny,)

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(PasswordChangeView, self).dispatch(*args, **kwargs)

    def post(self, request):
        print request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        messages.add_message(request, messages.INFO, 'Inicia sesión con tu nueva contraseña')
        return Response({"detail": _("New password has been saved.")})

class FacebookAuth(SocialLoginView):   
    adapter_class = FacebookOAuth2Adapter

class GoogleAuth(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    
    def __init__(self):
        self.callback_url = self.get_callback_url()
    
    def get_callback_url(self):
        domain = Site.objects.get_current().domain
        return 'https://tu-mercado.co/api/accounts/google/login/callback/'.format(domain=domain)