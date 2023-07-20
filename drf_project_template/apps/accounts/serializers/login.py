from rest_framework import serializers, exceptions
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from dj_rest_auth.serializers import LoginSerializer as DJRestLoginSerializer

from drf_project_template.apps.accounts.models import User


DEBUG = settings.DEBUG
class PreLoginSerializer(DJRestLoginSerializer):
    username = None
    email = serializers.EmailField(label=_("email"), write_only=True, required=True)

    def validate_phone_verification_status(self, user: "User"):
        if not user.phone_number_verified:
            raise exceptions.ValidationError(
                 _("Phone number not verified."), code="phone_not_verified"
            )

    def validate_email_verification_status(self, user: "User"):
        try:
            return super().validate_email_verification_status(user)
        except exceptions.ValidationError as e:
            raise exceptions.ValidationError(
                _("Please verify your email."), code="email_not_verified"
            )

    def validate(self, attrs):
        username: str = attrs.get("username")
        email: str = attrs.get("email")
        password: str = attrs.get("password")
        user: "User" = self.get_auth_user(username, email, password)

        if not user:
            msg = _("Unable to log in with provided credentials.")
            raise exceptions.ValidationError(msg)

        # Did we get back an active user?
        self.validate_auth_user_status(user)

        # superuser bypass
        if not user.is_superuser:
            self.validate_email_verification_status(user)
            self.validate_phone_verification_status(user)

        attrs["user"] = user
        return attrs

    @staticmethod
    def mfa_required(user: "User") -> bool:
        _user_profile = getattr(user, "profile", None)
        if _user_profile:
            return _user_profile.mfa_required
        return False

class LoginSerializer(PreLoginSerializer):
    mfa_code = serializers.CharField(required=False)

    def validate(self, attrs):
        attrs = super(LoginSerializer, self).validate(attrs)

        user: "User" = attrs.get("user")
        mfa_required: bool = self.mfa_required(user)
        mfa_code: str = attrs.get("mfa_code")

        if mfa_required and not DEBUG:

            if not mfa_code:
                msg = _("OTP code is required")
                raise serializers.ValidationError(msg, code="authorization")
            mfa_valid = user.verify_totp_code(mfa_code)

            if not mfa_valid:
                _msg = _("OTP is invalid or has expired")
                raise serializers.ValidationError(_msg, code="authorization")

        return attrs

