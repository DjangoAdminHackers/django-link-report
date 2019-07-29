
from django.core.management.base import BaseCommand

from ...utils import update_sentry_404s


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        update_sentry_404s()
