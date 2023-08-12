from django.core.management.base import BaseCommand

from ._notifications import notify


class Command(BaseCommand):
    help = "Sends notifications"

    def handle(self, *args, **options):
        notify()
