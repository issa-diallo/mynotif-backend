import os

from django.http import JsonResponse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from main.serializers import CustomAuthTokenSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def version(_request):
    version = os.environ.get("VERSION") or "0.0.0"
    return JsonResponse({"version": version})


class CustomObtainAuthToken(ObtainAuthToken):
    """
    Override rest_framework.authtoken.views.ObtainAuthToken to authenticate via email
    and password.
    """

    serializer_class = CustomAuthTokenSerializer
