from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class AccountAdapter(DefaultAccountAdapter):

    def get_email_confirmation_redirect_url(self, request):
        return reverse('webclient:login')

class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def get_connect_redirect_url(self, request):
        return reverse('webclient:home')

    def save_user(self, request, sociallogin, form=None):
        super(DefaultSocialAccountAdapter, self).save_user(request, sociallogin, form=form)
        return redirect(reverse('webclient:home'))