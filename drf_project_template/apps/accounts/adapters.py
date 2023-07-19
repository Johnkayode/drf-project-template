from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings

from allauth import app_settings as allauth_settings
from allauth.account.adapter import DefaultAccountAdapter



class AccountAdapter(DefaultAccountAdapter):
    def clean_email(self, email):
        if isinstance(email, str):
            return email.lower()
        return email

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        current_site = get_current_site(request)
        activate_url = self.get_email_confirmation_url(request, emailconfirmation)
        link_expiry = getattr(
            allauth_settings, "ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS", 3
        )

        ctx = {
            "user": emailconfirmation.email_address.user,
            "activate_url": activate_url,
            "current_site": current_site,
            "key": emailconfirmation.key,
            "frontend_url": settings.FRONTEND_URL,
            "expiry": f"{link_expiry} days",
            "support_email": getattr(
                settings, "SUPPORT_EMAIL", "support@bridger.africa"
            ),
        }
        
        email_template = "account/email/email_confirmation_signup"
        self.send_mail(email_template, emailconfirmation.email_address.email, ctx)