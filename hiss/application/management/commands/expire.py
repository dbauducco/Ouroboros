from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import QuerySet

from application.models import Application, STATUS_ADMITTED, STATUS_EXPIRED


def expire_apps(queryset: QuerySet) -> QuerySet:
    """
    Changes all of the members of the provided QuerySet from their current status to STATUS_EXPIRED.
    :param queryset: The queryset of applications to mark as STATUS_EXPIRED
    :return: The updated queryset.
    """
    expired = queryset.update(status=STATUS_EXPIRED)
    return expired


class Command(BaseCommand):
    """
    A Django management command that takes all of the applicants whose confirmation deadlines have passed,
    and have yet to confirm their spot, and expires them.

    This function is best run as a cron job, so that applications are constantly being monitored to be expired,
    but can be run manually. If run as a cron job, don't forget to send STDOUT and STDERR output to a file you can
    access, for debugging purposes.
    """

    def handle(self, *args, **options):
        unconfirmed = Application.objects.filter(
            status=STATUS_ADMITTED, confirmation_deadline__lt=timezone.now()
        )
        self.stdout.write("Going to expire %s applications" % (unconfirmed.count()))
        expired = expire_apps(unconfirmed)
        self.stdout.write(
            self.style.SUCCESS("All %s applications successfully expired" % expired)
        )
