import os
from unittest import mock

import pytest
from django.urls import reverse_lazy
from rest_framework import status


class TestVersion:
    url = "/api/v1/version/"

    def test_endpoint(self):
        assert self.url == reverse_lazy("v1:version")

    @pytest.mark.parametrize(
        "env,expected",
        [
            # default return
            ({}, "0.0.0"),
            ({"VERSION": ""}, "0.0.0"),
            # base case
            ({"VERSION": "1.2.3"}, "1.2.3"),
        ],
    )
    def test_version(self, client, env, expected):
        with mock.patch.dict(os.environ, env):
            response = client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"version": expected}
        with mock.patch.dict(os.environ, env):
            response = client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"version": expected}


class TestError400View:
    url = "/api/v1/error-400/"

    def test_endpoint(self):
        assert self.url == reverse_lazy("v1:error_400")

    def test_400(self, client):
        """
        Raising a `django.core.exceptions.BadRequest` without implementing
        `rest_framework.views.APIView` should still return a `JsonResponse`.
        """
        response = client.get(self.url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"error": "Bad Request (400)"}


class TestError400APIView:
    url = "/api/v1/api-error-400/"

    def test_endpoint(self):
        assert self.url == reverse_lazy("v1:api_error_400")

    def test_api_400(self, client):
        """
        Views raising a `django.core.exceptions.BadRequest` should return a
        `JsonResponse` as long as they implement the `rest_framework.views.APIView`.
        """
        response = client.get(self.url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"error": "Bad Request (400)"}


class TestError404View:
    url = "/api/v1/error-404/"

    def test_endpoint(self):
        assert self.url == reverse_lazy("v1:error_404")

    def test_404(self, client):
        """
        Raising a `django.http.Http404` without implementing
        `rest_framework.views.APIView` should return an HTML response.
        """
        response = client.get(self.url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.content.decode("utf-8").split("\n") == [
            "",
            "<!doctype html>",
            '<html lang="en">',
            "<head>",
            "  <title>Not Found</title>",
            "</head>",
            "<body>",
            "  <h1>Not Found</h1>"
            + "<p>The requested resource was not found on this server.</p>",
            "</body>",
            "</html>",
            "",
        ]


class TestError404APIView:
    url = "/api/v1/api-error-404/"

    def test_endpoint(self):
        assert self.url == reverse_lazy("v1:api_error_404")

    def test_api_404(self, client):
        """
        Views raising a `django.http.Http404` should return a `JsonResponse` as long as
        they implement the `rest_framework.views.APIView`.
        """
        response = client.get(self.url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data == {
            "detail": "This is an uncaught 404 exception for testing."
        }


class TestError500View:
    url = "/api/v1/error-500/"

    def test_endpoint(self):
        assert self.url == reverse_lazy("v1:error_500")

    def test_500(self, client):
        """
        Raising an exception without implementing `rest_framework.views.APIView`
        should still return a `JsonResponse` thanks to the urls `handler500`
        `rest_framework.exceptions.server_error`.
        """
        client.raise_request_exception = False
        response = client.get(self.url)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"error": "Server Error (500)"}


class TestError500APIView:
    url = "/api/v1/api-error-500/"

    def test_endpoint(self):
        assert self.url == reverse_lazy("v1:api_error_500")

    def test_api_500(self, client):
        """
        Raising an uncaught exception should return a `JsonResponse` for views
        implementing `rest_framework.views.APIView`.
        """
        client.raise_request_exception = False
        response = client.get(self.url)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"error": "Server Error (500)"}
