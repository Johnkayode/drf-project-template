import uuid
import pyotp
from allauth.account.models import EmailAddress
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.phonenumber import PhoneNumber

from drf_project_template.apps.accounts.utils import generate_public_id



class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    phone_number = PhoneNumberField(_("phone number"), blank=True)
    phone_number_verified = models.BooleanField(default=False)

    uid = models.UUIDField(unique=True, editable=False, null=True, default=uuid.uuid4)
    public_id = models.CharField(
        _("public id"),
        max_length=50,
        blank=True,
        default=generate_public_id,
        editable=False,
        unique=True,
    )
 
    password_change_required = models.BooleanField(default=False)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    
    @property
    def full_name(self) -> str:
        return self.get_full_name()

    @property
    def email_verified(self) -> bool:
        return EmailAddress.objects.filter(email=self.email, verified=True).exists()

    @property
    def first_time_login(self) -> bool:
        return self.last_login is None
        
    @property
    def has_profile(self) -> bool:
        """
        Checks if user's profile has been created
        """
        return hasattr(self, "profile")

    def get_basic_user_details(self) -> dict:
        return {
            "uid": self.uid,
            "email": self.email,
            "full_name": self.full_name,
            "phone": self.phone_number,
            "public_id": self.public_id,
        }