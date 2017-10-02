# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from allauth.socialaccount import providers
from allauth.socialaccount.models import SocialLogin, SocialToken, SocialApp
from allauth.socialaccount.providers.facebook.views import fb_complete_login
from allauth.socialaccount.helpers import complete_social_login

from .serializers import AddressSerializer, AddressCreateSerializer
from .models import Address


class AddressCreate(generics.CreateAPIView):
    """Crea una dirección, asignada al usuario del token de autenticación enviado
    """

    serializer_class = AddressCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.auth.user)

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

class FacebookAuth(APIView):   
    
    def dispatch(self, *args, **kwargs):
        return super(FacebookAuth, self).dispatch(*args, **kwargs)
    
    def post(self, request):        
        access_token = request.POST.get('access_token', '')    
        
        try:
            app = SocialApp.objects.get(provider="facebook")
            token = SocialToken(app=app, token=access_token)
                            
            # check token against facebook                  
            login = fb_complete_login(app, token)
            login.token = token
            login.state = SocialLogin.state_from_request(request)
        
            # add or update the user into users table
            ret = complete_social_login(request, login)
 
            # if we get here we've succeeded
            return Response(status=200, data={
                'success': True,
                'username': request.user.username,
                'user_id': request.user.pk,
            })
            
        except:
 
            return Response(status=401 ,data={
                'success': False,
                'reason': "Bad Access Token",
            })