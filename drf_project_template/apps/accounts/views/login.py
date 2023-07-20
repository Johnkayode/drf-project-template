from typing import Optional, Dict, Any, TYPE_CHECKING

from rest_framework import permissions, status, generics, response
from django.conf import settings
from drf_project_template.apps.accounts.serializers import PreLoginSerializer

if TYPE_CHECKING:
    from drf_project_template.apps.accounts.models import User

DEBUG = settings.DEBUG

class PreLoginView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []
    serializer_class = PreLoginSerializer


    def post(self, request, format=None):
        serializer = self.get_serializer(
            data=request.data, context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)

        user: "User" = serializer.validated_data["user"]
        self._user: "User" = user
        mfa_required: bool = self.mfa_required(user)

        if mfa_required and not DEBUG:
            self.send_otp(medium = "phone")
            return response.Response(
                {
                    "detail": "A six digit OTP has been sent to your email address",
                    "data": None,
                    "message": "mfa required"
                },
                status.HTTP_201_CREATED,
            )

    def send_otp(self, medium: str) -> Optional[dict]:
        return self._user.dispatch_otp(medium)

    def mfa_required(self, user: "User") -> bool:
        # TODO: Implement in user profile
        return True


class LoginView():
    pass