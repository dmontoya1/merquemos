from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.urls import reverse
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.helpers import complete_social_login, login_social_account

class AccountAdapter(DefaultAccountAdapter):

    def get_email_confirmation_redirect_url(self, request):
        return reverse('webclient:login')

class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def get_connect_redirect_url(self, request):
        return reverse('webclient:home')

    def save_user(self, request, sociallogin, form=None):
        super(DefaultSocialAccountAdapter, self).save_user(request, sociallogin, form=form)
        return redirect(reverse('webclient:home'))

    def pre_social_login(self, request, sociallogin):
        try:
            user = get_user_model().objects.get(username=sociallogin.user.email)
        except get_user_model().DoesNotExist:
            existing_user = False

        if existing_user:
            sociallogin.connect(request, user)
            return login_social_account(request, user)
        
        pass
        
