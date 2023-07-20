from rest_framework import permissions, status, generics
from drf_project_template.apps.accounts.serializers import PreLoginSerializer

class PreLoginView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []
    serializer_class = PreLoginSerializer


    