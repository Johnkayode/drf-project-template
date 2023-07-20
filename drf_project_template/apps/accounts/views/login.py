from typing import Optional, Dict, Any, TYPE_CHECKING

from rest_framework import permissions, status, generics, response
from drf_project_template.apps.accounts.serializers import PreLoginSerializer

if TYPE_CHECKING:
    from drf_project_template.apps.accounts.models import User


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

        self.send_otp(medium = "phone")
        return response.Response(
            {
                "detail": "A six digit OTP has been sent to your email address",
                "data": None
            },
            status.HTTP_201_CREATED,
        )

    def send_otp(self, medium: str) -> Optional[dict]:
        return self._user.dispatch_otp(medium)