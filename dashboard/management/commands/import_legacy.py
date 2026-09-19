import sqlite3
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from analysis.cities import TDX_CITIES
from dashboard.models import (
    City,
    HouseholdIncome,
    PopulationStat,
    StudentStatus,
    VehicleCount,
)

DEFAULT_LEGACY = (
    Path(settings.BASE_DIR) / "original-data" / "python-10" / "db.sqlite3"
)


def _int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


class Command(BaseCommand):
    help = (
        "Import 2023 course data from original-data/python-10/db.sqlite3. "
        "Skips auth tables and TDX API keys."
    )

    def add_arguments(self, parser):
        parser.add_argument("--db", type=str, default=str(DEFAULT_LEGACY))

    def handle(self, *args, **options):
        path = Path(options["db"])
        if not path.exists():
            raise CommandError(f"Legacy database not found: {path}")

        source = sqlite3.connect(path)
        source.row_factory = sqlite3.Row

        created_cities = 0
        for english, chinese in TDX_CITIES:
            _, created = City.objects.update_or_create(
                english_name=english,
                defaults={"chinese_name": chinese},
            )
            created_cities += int(created)

        vehicles = 0
        for row in source.execute("SELECT * FROM mysite_vehicle"):
            VehicleCount.objects.update_or_create(
                year=_int(row["year"]),
                month=_int(row["month"]),
                city_name=row["city_name"],
                vehicle_type=row["vehicle_type"],
                defaults={
                    "county_code": row["county_code"] or "",
                    "value": _int(row["value"]),
                },
            )
            vehicles += 1

        incomes = 0
        for row in source.execute("SELECT * FROM mysite_household_income"):
            HouseholdIncome.objects.update_or_create(
                year=_int(row["year"]),
                city_name=row["city_name"],
                defaults={
                    "county_code": row["county_code"] or "",
                    "avg_households": _float(row["Avg_number_of_househods"]),
                    "avg_employment": _float(row["Avg_number_of_employment"]),
                    "avg_income_earners": _float(row["Avg_number_of_income"]),
                    "total": _float(row["Total"]),
                },
            )
            incomes += 1

        students = 0
        for row in source.execute(
            "SELECT * FROM mysite_universities_and_colleges_student_status"
        ):
            StudentStatus.objects.update_or_create(
                year=_int(row["year"]),
                city_name=row["city_name"],
                school_code=row["SchoolCode"] or "",
                defaults={
                    "county_code": row["county_code"] or "",
                    "school_type": row["type"] or "",
                    "school_name": row["SchoolName"] or "",
                    "males": _int(row["NumberOfMales"]),
                    "females": _int(row["NumberOfFemales"]),
                    "total": _int(row["Total"]),
                },
            )
            students += 1

        population = 0
        for row in source.execute("SELECT * FROM mysite_population_stats"):
            PopulationStat.objects.update_or_create(
                year=_int(row["Year"]),
                month=_int(row["Month"]),
                town_code=row["TownCode"] or "",
                defaults={
                    "city_name": row["CityName"],
                    "county_code": row["CountyCode"] or "",
                    "town_name": row["TownName"] or "",
                    "households": _int(row["NumberOfHousehods"]),
                    "population": _int(row["NumberOfPopulation"]),
                    "males": _int(row["NumberOfMales"]),
                    "females": _int(row["NumberOfFemales"]),
                },
            )
            population += 1

        source.close()
        self.stdout.write(
            self.style.SUCCESS(
                "Imported cities=%s vehicles=%s income=%s students=%s population=%s. "
                "TDX keys and auth tables were not copied."
                % (created_cities, vehicles, incomes, students, population)
            )
        )
