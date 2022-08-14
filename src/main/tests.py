import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls.base import reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient


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


class TestApiTokenAuth:

    client = APIClient()
    url = "/api-token-auth/"

    def test_endpoint(self):
        assert reverse_lazy("api_token_auth") == self.url

    @pytest.mark.django_db
    def test_invalid(self):
        return
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
        return
        data = {
            "username": "username",
            "password": "password",
        }
        user = User.objects.create(username=data["username"])
        user.set_password(data["password"])
        user.save()
        response = self.client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data.keys() == {"token"}
