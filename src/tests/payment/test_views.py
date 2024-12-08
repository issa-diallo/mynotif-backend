from unittest import mock
from unittest.mock import MagicMock, patch

import pytest
import stripe
from django.urls.base import reverse_lazy
from rest_framework import status

from payment.models import StripeProduct, Subscription


@pytest.fixture
def client(authenticated_client):
    return authenticated_client


@pytest.mark.django_db
class TestSubscriptionViewSet:

    create_url = reverse_lazy("v1:payment:subscription-list")
    cancel_user_url = reverse_lazy("v1:payment:subscription-user-cancel")

    def test_endpoint(self):
        assert self.create_url == "/api/v1/payment/subscription/"

    def test_endpoint2(self):
        assert self.cancel_user_url == "/api/v1/payment/subscriptions/user/cancel/"

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

    @mock.patch("stripe.Subscription.modify")
    def test_subscription_user_cancel_view(self, mock_stripe_modify, client, user):
        client.force_login(user)

        subscription = Subscription.objects.create(
            user=user,
            stripe_subscription_id="sub_1FgsVx2R1LZ5sbG0fFqkg9Jz",
            cancel_at_period_end=False,
        )

        mock_stripe_modify.return_value = {
            "id": "sub_1FgsVx2R1LZ5sbG0fFqkg9Jz",
            "cancel_at_period_end": True,
        }

        response = client.post(self.cancel_user_url, data={}, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Subscription cancelled successfully"

        subscription.refresh_from_db()
        assert subscription.cancel_at_period_end is True

    @mock.patch("stripe.Subscription.modify")
    def test_subscription_user_cancel_stripe_error(
        self, mock_stripe_modify, client, user
    ):
        client.force_login(user)

        subscription = Subscription.objects.create(
            user=user,
            stripe_subscription_id="sub_1FgsVx2R1LZ5sbG0fFqkg9Jz",
            cancel_at_period_end=False,
        )

        mock_stripe_modify.side_effect = stripe.error.InvalidRequestError(
            "Invalid subscription ID", "param"
        )

        response = client.post(self.cancel_user_url, data={}, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Stripe error: Invalid subscription ID"

        subscription.refresh_from_db()
        assert subscription.cancel_at_period_end is False

    @mock.patch("stripe.Subscription.modify")
    def test_subscription_user_cancel_unknown_error(
        self, mock_stripe_modify, client, user
    ):
        client.force_login(user)

        subscription = Subscription.objects.create(
            user=user,
            stripe_subscription_id="sub_1FgsVx2R1LZ5sbG0fFqkg9Jz",
            cancel_at_period_end=False,
        )

        mock_stripe_modify.side_effect = Exception("Something went wrong")

        response = client.post(self.cancel_user_url, data={}, format="json")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "An error occurred: Something went wrong"

        subscription.refresh_from_db()
        assert subscription.cancel_at_period_end is False
