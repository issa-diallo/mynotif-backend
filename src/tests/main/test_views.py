from unittest import mock

import pytest
from django.urls.base import reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient


class TestVersion:
    client = APIClient()
    url = "/version/"

    def test_endpoint(self):
        assert reverse_lazy("version") == self.url

    @pytest.mark.parametrize(
        "env_version,expected_version",
        [
            ("1.2.3", "1.2.3"),
            ("", "0.0.0"),
        ],
    )
    def test_backend_url(self, env_version, expected_version):
        with mock.patch.dict("os.environ", {"VERSION": env_version}):
            response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"version": expected_version}
