import typing
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
    
    def get_response_data(self, user: "User") -> typing.Dict[str, str]:
        return {"detail": _("Registration Successful, Proceed to login")}