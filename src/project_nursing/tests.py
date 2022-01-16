from django.test import Client
from django.urls.base import reverse_lazy
from rest_framework import status


class TestDocumentation:

    client = Client()
    url_openapi = "/openapi"
    url_redoc = "/redoc/"
    url_swagger = "/swagger/"

    def test_openapi(self):
        assert reverse_lazy("openapi-schema") == self.url_openapi
        response = self.client.get(self.url_openapi)
        assert response.status_code == status.HTTP_200_OK

    def test_redoc(self):
        assert reverse_lazy("schema-redoc") == self.url_redoc
        response = self.client.get(self.url_redoc)
        assert response.status_code == status.HTTP_200_OK

    def test_swagger(self):
        assert reverse_lazy("schema-swagger-ui") == self.url_swagger
        response = self.client.get(self.url_swagger)
        assert response.status_code == status.HTTP_200_OK
