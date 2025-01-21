from django.urls import include, path
from rest_framework import routers

from payment.views import SubscriptionUserCancelView, SubscriptionViewSet

from . import webhooks

router = routers.DefaultRouter()
router.register("subscription", SubscriptionViewSet)

app_name = "payment"

urlpatterns = [
    path("", include(router.urls)),
    path(
        "subscriptions/user/cancel/",
        SubscriptionUserCancelView.as_view(),
        name="subscription-user-cancel",
    ),
    path("stripe/webhook/", webhooks.stripe_webhook, name="stripe-webhook"),
]

urlpatterns += router.urls
