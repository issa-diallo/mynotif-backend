import pytest
from django.contrib.auth.models import User
from django.core import mail
from django.test import Client, override_settings
from django.urls.base import reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient


def user_create(username, password):
    """Creates a user and returns it."""
    user = User.objects.create(username=username)
    user.set_password(password)
    user.save()
    return user


class TestDocumentation:
    client = Client()
    url_redoc = "/redoc/"
    url_swagger = "/swagger/"

    def test_redoc(self):
        assert reverse_lazy("schema-redoc") == self.url_redoc
        response = self.client.get(self.url_redoc)
        assert response.status_code == status.HTTP_200_OK

    def test_swagger(self):
        assert reverse_lazy("schema-swagger-ui") == self.url_swagger
        response = self.client.get(self.url_swagger)
        assert response.status_code == status.HTTP_200_OK


class TestApiTokenAuthV1:
    client = APIClient()
    url = "/api/v1/api-token-auth/"

    def test_endpoint(self):
        assert reverse_lazy("v1:api_token_auth") == self.url

    @pytest.mark.django_db
    def test_invalid(self):
        data = {
            "username": "username",
            "password": "password",
        }
        response = self.client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.data["non_field_errors"][0]
            == "Unable to log in with provided credentials."
        )

    @pytest.mark.django_db
    def test_valid(self):
        data = {
            "username": "username",
            "password": "password",
        }
        user_create(data["username"], data["password"])
        response = self.client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data.keys() == {"token"}


class TestApiTokenAuthV2:
    client = APIClient()
    url = "/api/v2/api-token-auth/"

    def test_endpoint(self):
        assert reverse_lazy("v2:api_token_auth") == self.url

    @pytest.mark.django_db
    def test_invalid(self):
        data = {
            "email": "foo@bar.com",
            "password": "password",
        }
        response = self.client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.data["non_field_errors"][0]
            == "Unable to log in with provided credentials."
        )

    @pytest.mark.django_db
    def test_valid(self):
        data = {
            "email": "foo@bar.com",
            "password": "password",
        }
        user_create(data["email"], data["password"])
        response = self.client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data.keys() == {"token"}


class TestDjoser:
    client = APIClient()
    url = "/api/v1/auth/"
    namespace = "v1:auth"

    def test_endpoint(self):
        assert reverse_lazy(f"{self.namespace}:api-root") == self.url

    @override_settings(
        DJOSER={"PASSWORD_RESET_CONFIRM_URL": "/reset/password/{uid}/{token}"}
    )
    @pytest.mark.django_db
    def test_reset_password(self):
        url = reverse_lazy(f"{self.namespace}:user-reset-password")
        assert url == "/api/v1/auth/users/reset_password/"
        username = "username"
        password = "password"
        email = "email@foo.com"
        user = user_create(username, password)
        user.email = email
        user.save()
        data = {
            "email": email,
        }
        assert len(mail.outbox) == 0
        response = self.client.post(url, data, format="json")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == "Password reset on testserver"
