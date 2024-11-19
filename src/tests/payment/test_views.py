from unittest.mock import MagicMock, patch

import pytest
from django.contrib.auth.models import User
from django.urls.base import reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient

from payment.models import StripeProduct, Subscription

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


@pytest.fixture
def staff_user(user):
    """Creates and yields a staff user."""
    user.is_staff = True
    user.save()
    yield user


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
def authenticated_client(user):
    """Authenticates the user via token and yields it."""
    client = APIClient()
    client = authenticate_client_with_token(client, user.email, PASSWORD)
    yield client
    # invalidates credentials
    client.credentials()


@pytest.fixture
def client(authenticated_client):
    return authenticated_client


@pytest.mark.django_db
class TestSubscriptionViewSet:

    create_url = reverse_lazy("v1:payment:subscription-list")

    def retrieve_url(self, pk):
        return reverse_lazy("v1:payment:subscription-detail", kwargs={"pk": pk})

    @patch("payment.views.stripe.checkout.Session.create")
    @patch("payment.views.StripeProduct.objects.get")
    def test_create_subscription_success(
        self, mock_get_product, mock_create_session, client, user
    ):
        client.force_login(user)
        data = {"plan": "monthly"}
        mock_checkout_session = MagicMock()
        mock_checkout_session.id = "session_id_example"
        mock_checkout_session.url = "https://checkout.stripe.com/pay/example"
        mock_create_session.return_value = mock_checkout_session
        response = client.post(self.create_url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["sessionId"] == "session_id_example"
        assert (
            response.data["checkout_url"] == "https://checkout.stripe.com/pay/example"
        )

    @patch("payment.views.stripe.checkout.Session.create")
    @patch("payment.views.StripeProduct.objects.get")
    def test_create_subscription_product_not_found(
        self, mock_get_product, mock_create_session, client, user
    ):
        client.force_login(user)
        data = {"plan": "monthly"}
        mock_get_product.side_effect = StripeProduct.DoesNotExist
        response = client.post(self.create_url, data, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"] == "Product not found"

    @patch("payment.views.stripe.checkout.Session.create")
    @patch("payment.views.StripeProduct.objects.get")
    def test_create_subscription_stripe_session_creation_failed(
        self, mock_get_product, mock_create_session, client, user
    ):
        client.force_login(user)
        data = {"plan": "monthly"}
        mock_product = MagicMock()
        mock_product.monthly_price_id = "price_monthly_id_example"
        mock_product.annual_price_id = "price_annual_id_example"
        mock_get_product.return_value = mock_product
        mock_create_session.side_effect = Exception("Error during session creation")
        response = client.post(self.create_url, data, format="json")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Error during session creation" in response.data["error"]

    @patch("payment.views.stripe.checkout.Session.create")
    @patch("payment.views.StripeProduct.objects.get")
    def test_retrieve_subscription_success(
        self, mock_get_product, mock_create_session, client, user
    ):
        client.force_login(user)
        subscription = Subscription.objects.create(
            user=user, stripe_subscription_id="session_id_example"
        )
        response = client.get(self.retrieve_url(subscription.pk), format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["user"] == user.id
        assert response.data["stripe_subscription_id"] == "session_id_example"

    def test_retrieve_subscription_not_found(self, client, user):
        client.force_login(user)
        response = client.get(self.retrieve_url(9999), format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_subscription_success_view(self, client):
        response = client.get("/api/v1/payment/subscriptions/success/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Subscription successful"

    def test_subscription_cancel_view(self, client):
        response = client.get("/api/v1/payment/subscriptions/cancel/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Subscription cancelled"


@pytest.fixture
def stripe_product():
    return StripeProduct.objects.create(
        name="Product 1",
        product_id="prod_test_id",
        monthly_price_id="price_test_monthly",
        annual_price_id="price_test_annual",
    )


@pytest.mark.django_db
class TestStripeProductViewSet:

    def test_create_stripe_product(self, client, staff_user):
        url = reverse_lazy("v1:payment:stripeproduct-list")
        data = {
            "name": "Product 1",
            "product_id": "prod_test_id",
            "monthly_price_id": "price_test_monthly",
            "annual_price_id": "price_test_annual",
        }
        client.force_authenticate(user=staff_user)
        response = client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "Product 1"
        assert response.data["product_id"] == "prod_test_id"
        assert response.data["monthly_price_id"] == "price_test_monthly"
        assert response.data["annual_price_id"] == "price_test_annual"

    def test_list_stripe_products(self, client, staff_user, stripe_product):
        url = reverse_lazy("v1:payment:stripeproduct-list")
        client.force_authenticate(user=staff_user)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["name"] == "Product 1"
        assert response.data[0]["product_id"] == "prod_test_id"

    def test_retrieve_stripe_product(self, client, staff_user, stripe_product):
        url = reverse_lazy(
            "v1:payment:stripeproduct-detail", kwargs={"pk": stripe_product.pk}
        )
        client.force_authenticate(user=staff_user)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Product 1"
        assert response.data["product_id"] == "prod_test_id"

    def test_update_stripe_product(self, client, staff_user, stripe_product):
        url = reverse_lazy(
            "v1:payment:stripeproduct-detail", kwargs={"pk": stripe_product.pk}
        )
        data = {
            "name": "Updated Product",
            "product_id": "updated_prod_id",
            "monthly_price_id": "updated_price_monthly",
            "annual_price_id": "updated_price_annual",
        }
        client.force_authenticate(user=staff_user)
        response = client.put(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Updated Product"
        assert response.data["product_id"] == "updated_prod_id"
        assert response.data["monthly_price_id"] == "updated_price_monthly"
        assert response.data["annual_price_id"] == "updated_price_annual"

    def test_delete_stripe_product(self, client, staff_user, stripe_product):
        url = reverse_lazy(
            "v1:payment:stripeproduct-detail", kwargs={"pk": stripe_product.pk}
        )
        client.force_authenticate(user=staff_user)
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert StripeProduct.objects.count() == 0
