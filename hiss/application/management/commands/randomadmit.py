from django.core.management.base import BaseCommand, CommandParser

from application.admin import approve
from application.models import Application, STATUS_PENDING


class Command(BaseCommand):
    """
    Approves the provided percentage of unreviewed applications. For example, if 0.20 is provided,
    and 100 applications are unreviewed, then 20 random applications are approved. If 100 applications have not been
    reviewed, and 0.50 is provided, then 50 random applications are approved.
    """

    def add_arguments(self, parser: CommandParser):
        parser.add_argument(
            "pct", type=float, help="Percentage of non-reviewed applications to admit"
        )

    def handle(self, *args, **options):
        # This can be inefficient depending on the DB backend used, but since this isn't intended to be used frequently,
        # it'll be fine.
        # https://docs.djangoproject.com/en/dev/ref/models/querysets/#django.db.models.query.QuerySet.order_by
        unreviewed = Application.objects.filter(status=STATUS_PENDING).order_by("?")
        num_unreviewed = unreviewed.count()
        num_to_approve = round(options["pct"] * num_unreviewed)
        self.stdout.write(
            "Going to approve %s applications (out of %s)"
            % (num_to_approve, num_unreviewed)
        )
        apps_to_approve = unreviewed[:num_to_approve]
        approve(None, None, apps_to_approve)
        self.stdout.write(
            self.style.SUCCESS(
                "All %s applications successfully approved" % num_to_approve
            )
        )
