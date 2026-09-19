from django.core.management.base import BaseCommand, CommandError

from fetchers.datasets import (
    fetch_income,
    fetch_population,
    fetch_students,
    fetch_vehicles,
    seed_cities,
)
from fetchers.tdx import TdxConfigError

DATASETS = {
    "vehicles": fetch_vehicles,
    "income": fetch_income,
    "students": fetch_students,
    "population": fetch_population,
}


class Command(BaseCommand):
    help = "Fetch TDX socio-economic datasets into the local database. Credentials come from .env."

    def add_arguments(self, parser):
        parser.add_argument(
            "dataset",
            nargs="?",
            default="all",
            choices=["all", *DATASETS],
        )

    def handle(self, *args, **options):
        seed_cities()
        names = DATASETS if options["dataset"] == "all" else [options["dataset"]]
        try:
            for name in names:
                stored = DATASETS[name]()
                self.stdout.write(self.style.SUCCESS(f"{name}: stored {stored} rows"))
        except TdxConfigError as exc:
            raise CommandError(str(exc)) from exc
