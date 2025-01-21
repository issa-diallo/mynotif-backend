import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from payment import constants
from payment.models import StripeProduct, Subscription
from payment.serializers import SubscriptionSerializer

ESSENTIAL_PLAN_NAME = "Essentiel"


class SubscriptionViewSet(viewsets.ModelViewSet):
    stripe.api_key = settings.STRIPE_API_KEY
    stripe.api_version = constants.STRIPE_API_VERSION
    plan_name = ESSENTIAL_PLAN_NAME

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user = request.user
        plan = request.data.get("plan")  # "monthly" ou "annual"
        product = get_object_or_404(StripeProduct, name=self.plan_name)
        price_id = (
            product.monthly_price_id if plan == "monthly" else product.annual_price_id
        )

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            customer_email=user.email,
            line_items=[{"price": price_id, "quantity": 1}],
            mode="subscription",
            billing_address_collection="required",
            currency="eur",
            success_url=f"{settings.FRONTEND_URL}/success?checkout=true",
            cancel_url=f"{settings.FRONTEND_URL}/cancel?checkout=true",
            metadata={
                "user_id": user.id,
                "product_name": product.name,
            },
        )

        return Response(
            {
                "sessionId": checkout_session.id,
                "checkout_url": checkout_session.url,
            },
            status=status.HTTP_201_CREATED,
        )

    def retrieve(self, request, *args, **kwargs):
        obj = get_object_or_404(self.get_queryset(), user=request.user)
        serializer = self.get_serializer(obj)
        return Response(serializer.data)


class SubscriptionUserCancelView(APIView):
    """
    Handles the cancelation of a subscription by the user.

    This endpoint is used to cancel a subscription by the user.
    It is called when the user requests to cancel their subscription.
    """

    def post(self, request, *args, **kwargs):
        user = request.user
        subscription = get_object_or_404(Subscription, user=user)
        stripe.api_key = settings.STRIPE_API_KEY

        try:
            stripe.Subscription.modify(
                subscription.stripe_subscription_id, cancel_at_period_end=True
            )

        except stripe.error.InvalidRequestError as e:
            return Response(
                {"error": f"Stripe error: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        subscription.cancel_at_period_end = True
        subscription.save()

        return Response(
            {"message": "Subscription canceled successfully"},
            status=status.HTTP_200_OK,
        )
