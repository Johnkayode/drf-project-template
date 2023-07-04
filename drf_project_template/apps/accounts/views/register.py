from rest_framework import (
    exceptions,
    permissions,
    response,
    views,
    status,
)



class RegistrationView(views.APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, *args, **kwargs):
        return response.Response(
            {
                "status": "OK",
                "message": "Server OK",
                "data": None
            },
            status=status.HTTP_200_OK,
        )