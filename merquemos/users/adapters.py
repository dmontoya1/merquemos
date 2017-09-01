from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from allauth.account.adapter import DefaultAccountAdapter

class AccountAdapter(DefaultAccountAdapter):

    def get_email_confirmation_redirect_url(self, request):
        messages.add_message(request, messages.SUCCESS, 'Cuenta activada exitosamente')
        return reverse('users:login')