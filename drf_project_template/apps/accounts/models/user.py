import uuid
from allauth.account.models import EmailAddress
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.utils import generate_public_id



class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(_("phone number"), blank=True)
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

    
    @property
    def full_name(self) -> str:
        return self.get_full_name()

    @property
    def email_verified(self) -> bool:
        return EmailAddress.objects.filter(email=self.email, verified=True).exists()

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