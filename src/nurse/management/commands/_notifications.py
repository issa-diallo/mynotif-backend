from django.conf import settings
from onesignal_sdk.client import Client

from nurse.models import Prescription, UserOneSignalProfile


def get_client():
    assert (app_id := settings.ONESIGNAL_APP_ID), "ONESIGNAL_APP_ID must be set"
    assert (api_key := settings.ONESIGNAL_API_KEY), "ONESIGNAL_API_KEY must be set"
    return Client(app_id=app_id, rest_api_key=api_key)


# Define notification messages for different languages
contents_dict = {
    "fr": (
        "Une ordonnance est sur le point d'expirer, "
        "ouvrez l'application pour la consulter."
    ),
    "en": ("A prescription is about to expire, open the app to review."),
}


def notify():
    """Notify nurses that have prescriptions to expire soon."""
    subscription_ids = set()
    prescriptions = Prescription.objects.expiring_soon()
    user_in = [
        nurse.user
        for prescription in prescriptions
        for nurse in prescription.patient.nurse_set.all()
    ]
    filter_args = {"user__in": user_in}
    subscription_id_list = UserOneSignalProfile.objects.filter(
        **filter_args
    ).values_list("subscription_id", flat=True)
    subscription_ids |= set(subscription_id_list)
    if subscription_ids:
        notification_body = {
            "contents": contents_dict,
            "include_subscription_ids": subscription_ids,
            "name": "PRESCRIPTION EXPIRE SOON",
        }
    get_client().send_notification(notification_body)


if __name__ == "__main__":
    notify()
