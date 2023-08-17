from unittest import mock

from django.core.management import call_command


class TestCommand:
    def test_notify_called(self):
        with mock.patch(
            "nurse.management.commands.send_notifications.notify"
        ) as mock_notify:
            call_command("send_notifications")
        assert mock_notify.call_args_list == [mock.call()]
