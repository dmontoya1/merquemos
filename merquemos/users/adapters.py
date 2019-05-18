from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse

from allauth.account.adapter import DefaultAccountAdapter, get_adapter
from allauth.account.utils import perform_login
from allauth.socialaccount import app_settings
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.helpers import complete_social_login
 

class AccountAdapter(DefaultAccountAdapter):

    def get_email_confirmation_redirect_url(self, request):
        return reverse('webclient:login')

class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def get_connect_redirect_url(self, request):
        return reverse('webclient:home')

    def save_user(self, request, sociallogin, form=None):
        u = sociallogin.user
        u.set_unusable_password()
        if form:
            get_adapter().save_user(request, u, form)
        else:
            get_adapter().populate_username(request, u)
        sociallogin.save(request)
        return redirect(reverse('webclient:home'))

    def pre_social_login(self, request, sociallogin):
        existing_user = True
        try:
            user = get_user_model().objects.get(email=sociallogin.user.email)
        except get_user_model().DoesNotExist:
            existing_user = False

        if existing_user:
            if not sociallogin.is_existing:
                sociallogin.connect(request, user)
            return perform_login(request, user, app_settings.EMAIL_VERIFICATION)
        
        pass
        
