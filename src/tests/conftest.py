import pytest
from django.contrib.auth.models import User
from django.urls.base import reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient

PASSWORD = "password1"
FIRSTNAME = "John"
LASTNAME = "Doe"
EMAIL = "johndoe@example.fr"
USERNAME = EMAIL
EMAIL_HOST_USER = "support@ordopro.fr"


@pytest.fixture
def user(db):
    """Creates and yields a new user."""
    user = User.objects.create(
        username=USERNAME, first_name=FIRSTNAME, last_name=LASTNAME, email=EMAIL
    )
    user.set_password(PASSWORD)
    user.save()
    yield user
    user.delete()


def authenticate_client_with_token(client, email, password):
    """Authenticates a client using a token and returns it."""
    # void previous credentials to avoid "Invalid token" errors
    client.credentials()
    response = client.post(
        reverse_lazy("v2:api_token_auth"),
        {"email": email, "password": password},
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    token = response.data["token"]
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    return client


@pytest.fixture
def staff_user(user):
    """Creates and yields a staff user."""
    user.is_staff = True
    user.save()
    yield user


@pytest.fixture
def authenticated_client(user):
    """Authenticates the user via token and yields it."""
    client = APIClient()
    client = authenticate_client_with_token(client, user.email, PASSWORD)
    yield client
    # invalidates credentials
    client.credentials()
