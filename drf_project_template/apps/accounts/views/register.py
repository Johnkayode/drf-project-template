from rest_framework import (
    exceptions,
    permissions,
    response,
    views,
    status,
)



class RegistrationView(views.APIView):
    
    def get(self, request, *args, **kwargs):
        return response.Response(
            {
                "status": "OK",
                "message": "Server OK",
            },
            status=status.HTTP_200_OK,
        )