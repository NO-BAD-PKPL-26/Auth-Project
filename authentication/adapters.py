from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.http import HttpResponseForbidden
import logging

logger = logging.getLogger(__name__)


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_auto_signup_allowed(self, request, sociallogin):
        return True 
    
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        email = data.get("email", "")

        if email:
            user.username = email.split("@")[0]

        return user

    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get("email", "")
        logger.info(f"Social login attempt: {email}")