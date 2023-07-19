import typing
from allauth.account.utils import complete_signup
from allauth.account import app_settings as allauth_settings
from django.utils.translation import gettext as _
from dj_rest_auth.registration import views as dj_rest_auth_registration_views
from rest_framework import (
    exceptions,
    permissions,
    response,
    views,
    status,
)

from drf_project_template.apps.accounts.serializers import RegisterSerializer
if typing.TYPE_CHECKING:
    from drf_project_template.apps.accounts.models import User



class RegisterView(dj_rest_auth_registration_views.RegisterView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def perform_create(self, serializer) -> "User":
        user: "User" = serializer.save(self.request)

        complete_signup(
            self.request._request,
            user,
            allauth_settings.EMAIL_VERIFICATION,
            None,
        )
        return user
    
    # def get_response_data(self, user: "User") -> typing.Dict[str, str]:
    #     return {"detail": _("Registration Successful, Proceed to login")}