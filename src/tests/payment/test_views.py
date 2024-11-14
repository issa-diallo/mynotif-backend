from unittest.mock import MagicMock, patch

import pytest
from django.urls.base import reverse_lazy
from rest_framework import status

from payment.models import StripeProduct, Subscription


@pytest.fixture
def client(authenticated_client):
    return authenticated_client


@pytest.mark.django_db
class TestSubscriptionViewSet:

    create_url = reverse_lazy("v1:payment:subscription-list")

    def test_endpoint(self):
        assert self.create_url == "/api/v1/payment/subscription/"

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
