import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import status, viewsets
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from payment.models import StripeProduct, Subscription
from payment.serializers import StripeProductSerializer, SubscriptionSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    stripe.api_key = settings.STRIPE_API_KEY
    stripe.api_version = settings.STRIPE_API_VERSION
    plan_name = settings.ESSENTIAL_PLAN_NAME

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user = request.user
        plan = request.data.get("plan")  # "monthly" ou "annual"

        try:
            product = StripeProduct.objects.get(name=self.plan_name)
            price_id = (
                product.monthly_price_id
                if plan == "monthly"
                else product.annual_price_id
            )
        except StripeProduct.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                customer_email=user.email,
                line_items=[{"price": price_id, "quantity": 1}],
                mode="subscription",
                billing_address_collection="required",
                currency="eur",
                success_url=request.build_absolute_uri(
                    reverse("v1:payment:subscription-success")
                ),
                cancel_url=request.build_absolute_uri(
                    reverse("v1:payment:subscription-cancel")
                ),
                metadata={
                    "user_id": user.id,
                    "product_name": product.name,
                },
            )

            data = {
                **request.data,
                "stripe_subscription_id": checkout_session.id,
            }

            headers = self.get_success_headers(data)
            return Response(
                {
                    "sessionId": checkout_session.id,
                    "checkout_url": checkout_session.url,
                },
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        except Exception as e:
            print("Error during session creation:", e)
            return Response({"error": str(e)}, status=500)

    def retrieve(self, request, *args, **kwargs):
        obj = get_object_or_404(self.get_queryset(), user=request.user)
        serializer = self.get_serializer(obj)
        return Response(serializer.data)


class SubscriptionSuccessView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(
            {"message": "Subscription successful"}, status=status.HTTP_200_OK
        )


class SubscriptionCancelView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(
            {"message": "Subscription cancelled"}, status=status.HTTP_200_OK
        )


class IsStaff(BasePermission):
    """
    Permission to check if the user is a staff member.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff


class StripeProductViewSet(viewsets.ModelViewSet):
    queryset = StripeProduct.objects.all()
    serializer_class = StripeProductSerializer
    permission_classes = [IsStaff]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
