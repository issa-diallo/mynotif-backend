from django.conf import settings
from onesignal_sdk.client import Client


def get_client():
    assert (app_id := settings.ONESIGNAL_APP_ID), "ONESIGNAL_APP_ID must be set"
    assert (api_key := settings.ONESIGNAL_API_KEY), "ONESIGNAL_API_KEY must be set"
    return Client(app_id=app_id, rest_api_key=api_key)


def notify():
    notification_body = {
        "contents": {
            "fr": "Une ordonnance est sur le point d'expirer, "
            "ouvrez l'application pour la consulter.",
            "en": "A prescription is about to expire open the app to review.",
        },
        "included_segments": ["Subscribed Users"],
        "name": "PRESCRIPTION EXPIRE SOON",
    }

    get_client().send_notification(notification_body)


if __name__ == "__main__":
    notify()
