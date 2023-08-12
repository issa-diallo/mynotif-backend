from unittest import mock

import pytest
from django.test import override_settings

from nurse.management.commands import _notifications

ONESIGNAL_APP_ID = "test_app_id"
ONESIGNAL_API_KEY = "test_api_key"
client_path = "nurse.management.commands._notifications.Client"


class TestNotifications:
    def test_notify(self):
        with mock.patch(
            f"{client_path}.send_notification"
        ) as mock_send_notification, override_settings(
            ONESIGNAL_APP_ID="ONESIGNAL_APP_ID", ONESIGNAL_API_KEY="ONESIGNAL_API_KEY"
        ):
            _notifications.notify()

        expected_notification_body = {
            "contents": {
                "fr": "Une ordonnance est sur le point d'expirer, "
                "ouvrez l'application pour la consulter.",
                "en": "A prescription is about to expire open the app to review.",
            },
            "included_segments": ["Subscribed Users"],
            "name": "PRESCRIPTION EXPIRE SOON",
        }

        assert mock_send_notification.call_args_list == [
            mock.call(expected_notification_body)
        ]

    def test_get_client_with_valid_settings():
        with override_settings(
            ONESIGNAL_APP_ID=ONESIGNAL_APP_ID,
            ONESIGNAL_API_KEY=ONESIGNAL_API_KEY,
        ), mock.patch(client_path) as mock_client:
            client = _notifications.get_client()

            mock_client.assert_called_once_with(
                app_id=ONESIGNAL_APP_ID, rest_api_key=ONESIGNAL_API_KEY
            )
            assert client == mock_client.return_value

    @pytest.mark.parametrize(
        "app_id, api_key, expected_error",
        [
            (None, ONESIGNAL_API_KEY, "ONESIGNAL_APP_ID must be set"),
            (ONESIGNAL_APP_ID, None, "ONESIGNAL_API_KEY must be set"),
        ],
    )
    def test_get_client_with_missing_settings(app_id, api_key, expected_error):
        with override_settings(
            ONESIGNAL_APP_ID=app_id,
            ONESIGNAL_API_KEY=api_key,
        ), pytest.raises(AssertionError, match=expected_error):
            _notifications.get_client()
