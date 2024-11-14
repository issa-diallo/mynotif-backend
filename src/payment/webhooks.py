import logging
from datetime import datetime

import stripe
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from helpers.model_utils import get_object_or_400
from payment.models import CustomerDetail, Subscription, User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_API_KEY
STRIPE_WEBHOOK_SECRET = settings.STRIPE_WEBHOOK_SECRET


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user = get_object_or_400(User, id=session["metadata"]["user_id"])
        CustomerDetail.objects.update_or_create(
            user=user,
            defaults={
                "stripe_customer_id": session["customer"],
                "city": session["customer_details"]["address"]["city"],
                "country": session["customer_details"]["address"]["country"],
                "address": session["customer_details"]["address"]["line1"],
                "postal_code": session["customer_details"]["address"]["postal_code"],
                "email": session["customer_details"]["email"],
            },
        )
        Subscription.objects.update_or_create(
            user=user,
            defaults={
                "stripe_subscription_id": session["subscription"],
                "status": session["status"],
                "payment_status": session["payment_status"],
                "product_name": session["metadata"]["product_name"],
                "total_price": session["amount_total"] / 100,
            },
        )

    elif event["type"] == "customer.subscription.updated":
        subscription_updated = event["data"]["object"]
        customer = get_object_or_400(
            CustomerDetail, stripe_customer_id=subscription_updated["customer"]
        )
        user = customer.user
        Subscription.objects.filter(user=user).update(
            cancel_at_period_end=subscription_updated["cancel_at_period_end"],
            current_period_start=timezone.make_aware(
                datetime.fromtimestamp(subscription_updated["current_period_start"])
            ),
            current_period_end=timezone.make_aware(
                datetime.fromtimestamp(subscription_updated["current_period_end"])
            ),
            trial_end=(
                timezone.make_aware(
                    datetime.fromtimestamp(subscription_updated["trial_end"])
                )
                if subscription_updated["trial_end"]
                and subscription_updated["trial_end"] != "null"
                else None
            ),
            active=bool(subscription_updated["items"]["data"][0]["plan"]["active"]),
        )

    elif event["type"] == "invoice.paid":
        invoice_paid = event["data"]["object"]
        customer = get_object_or_400(
            CustomerDetail, stripe_customer_id=invoice_paid["customer"]
        )
        user = customer.user
        Subscription.objects.filter(user=user).update(
            hosted_invoice_url=invoice_paid["hosted_invoice_url"],
            invoice_pdf=invoice_paid["invoice_pdf"],
        )

    elif event["type"] == "customer.subscription.deleted":
        subscription_deleted = event["data"]["object"]
        customer = get_object_or_400(
            CustomerDetail, stripe_customer_id=subscription_deleted["customer"]
        )
        user = customer.user
        Subscription.objects.filter(user=user).update(status="Cancelled", active=False)

    return HttpResponse(status=200)
