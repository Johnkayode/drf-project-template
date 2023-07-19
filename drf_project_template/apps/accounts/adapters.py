from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings

from allauth import app_settings as allauth_settings
from allauth.account.adapter import DefaultAccountAdapter
from phonenumber_field.phonenumber import PhoneNumber



class AccountAdapter(DefaultAccountAdapter):
    def clean_email(self, email):
        if isinstance(email, str):
            return email.lower()
        return email

    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        from .utils import user_email, user_field

        data = form.cleaned_data

        email = data.get("email")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        phone_number: PhoneNumber = data.get("phone_number")
        
        user_email(user, email)

        if first_name:
            user_field(user, "first_name", first_name)
        if last_name:
            user_field(user, "last_name", last_name)
        if phone_number:
            user_field(user, "phone_number", phone_number.as_e164)

        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        
        if commit:
            # Ability not to commit makes it easier to derive from
            # this adapter by adding
            user.save()
        return user

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
        
        if signup:
            email_template = "account/email/email_confirmation_signup"
        else:
            email_template = 'account/email/email_confirmation'
        self.send_mail(email_template, emailconfirmation.email_address.email, ctx)