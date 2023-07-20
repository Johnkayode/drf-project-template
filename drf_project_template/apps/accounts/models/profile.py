from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(
        UserModel, related_name="profile", on_delete=models.RESTRICT
    )
    mfa_required = models.BooleanField(default=False)

    #address
    address_street = models.CharField(max_length=100, blank=True, default="")
    address_city = models.CharField(max_length=100, blank=True, default="")
    address_state = models.CharField(max_length=100, blank=True, default="")
    address_lga = models.CharField(max_length=100, blank=True, default="")
    address_country = models.CharField(max_length=20, blank=False, default="NG")
    address_postal_code = models.CharField(max_length=100, blank=True, default="")
