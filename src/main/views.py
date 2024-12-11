import os

from django.core.exceptions import BadRequest
from django.http import Http404, JsonResponse
from django.views import View
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

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


class ErrorViewMixin:
    """Mixin to handle error-raising patterns for views."""

    exception_class = Exception
    exception_message = "An error occurred."

    def raise_exception(self):
        raise self.exception_class(self.exception_message)

    def get(self, request):
        self.raise_exception()


class Error400View(ErrorViewMixin, View):
    """Raise a 400 ValidationError while inheriting the regular Django View."""

    exception_class = BadRequest
    exception_message = "This is a bad request (400) for testing."


class Error400APIView(ErrorViewMixin, APIView):
    """Raise a 400 ValidationError while inheriting the DRF APIView."""

    permission_classes = [AllowAny]
    exception_class = BadRequest
    exception_message = "This is a bad request (400) for testing."


class Error404View(ErrorViewMixin, View):
    """Raise a regular django.http.Http404 while inheriting the regular Django View."""

    exception_class = Http404
    exception_message = "This is an uncaught 404 exception for testing."


class Error404APIView(ErrorViewMixin, APIView):
    """Raise a regular django.http.Http404 while inheriting the DRF APIView."""

    permission_classes = [AllowAny]
    exception_class = Http404
    exception_message = "This is an uncaught 404 exception for testing."


class Error500View(ErrorViewMixin, View):
    """Raise an uncaught exception while inheriting the regular Django View."""

    exception_class = ValueError
    exception_message = "This is an uncaught exception (500) for testing."


class Error500APIView(ErrorViewMixin, APIView):
    """Raise an uncaught exception while inheriting the DRF APIView."""

    permission_classes = [AllowAny]
    exception_class = ValueError
    exception_message = "This is an uncaught exception (500) for testing."
