from django.utils.translation import gettext as _
from dj_rest_auth.registration import views as dj_rest_auth_registration_views
from rest_framework import (
    response, 
    status
)



class VerifyEmailView(dj_rest_auth_registration_views.VerifyEmailView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs["key"] = serializer.validated_data["key"]
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        return response.Response(
            {"detail": _("ok"), "email": confirmation.email_address.email},
            status=status.HTTP_200_OK,
        )
