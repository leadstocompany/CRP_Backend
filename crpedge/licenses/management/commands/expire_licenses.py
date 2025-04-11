from django.core.management.base import BaseCommand
from django.utils import timezone
from licenses.models import License


class Command(BaseCommand):
    help = "Expire licenses whose end_date has passed."

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        expired = License.objects.filter(end_date__lt=today, status='active')
        count = expired.update(status='expired')

        self.stdout.write(self.style.SUCCESS(f"{count} license(s) expired."))
