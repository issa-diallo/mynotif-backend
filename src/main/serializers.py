from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer


class CustomAuthTokenSerializer(AuthTokenSerializer):
    """
    Override rest_framework.authtoken.serializers.AuthTokenSerializer to authenticate
    via email and password.
    """

    username = None
    email = serializers.EmailField(label=_("Email"), write_only=True)

    def validate(self, attrs):
        """Map email to username for compatibility with AuthTokenSerializer logic."""
        attrs["username"] = attrs.get("email")
        return super().validate(attrs)
