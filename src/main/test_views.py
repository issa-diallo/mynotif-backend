import os
from unittest import mock

import pytest
from django.urls import reverse
from rest_framework import status


class TestViews:
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
            response = client.get(reverse("version"))
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"version": expected}
        with mock.patch.dict(os.environ, env):
            response = client.get(reverse("version"))
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"version": expected}
