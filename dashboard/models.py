from django.db import models


class City(models.Model):
    english_name = models.CharField(max_length=64, unique=True)
    chinese_name = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.chinese_name} ({self.english_name})"


class VehicleCount(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    city_name = models.CharField(max_length=64, db_index=True)
    county_code = models.CharField(max_length=32, blank=True)
    vehicle_type = models.CharField(max_length=64)
    value = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["year", "month", "city_name", "vehicle_type"],
                name="uniq_vehicle_period_city_type",
            )
        ]
        indexes = [
            models.Index(fields=["year", "month"]),
        ]

    def __str__(self):
        return f"{self.year}-{self.month:02d} {self.city_name} {self.vehicle_type}"


class HouseholdIncome(models.Model):
    year = models.IntegerField()
    city_name = models.CharField(max_length=64, db_index=True)
    county_code = models.CharField(max_length=32, blank=True)
    avg_households = models.FloatField()
    avg_employment = models.FloatField()
    avg_income_earners = models.FloatField()
    total = models.FloatField(help_text="Household income total, million TWD")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["year", "city_name"], name="uniq_income_year_city")
        ]

    def __str__(self):
        return f"{self.year} {self.city_name}"


class StudentStatus(models.Model):
    year = models.IntegerField()
    city_name = models.CharField(max_length=64, db_index=True)
    county_code = models.CharField(max_length=32, blank=True)
    school_type = models.CharField(max_length=64, blank=True)
    school_code = models.CharField(max_length=64)
    school_name = models.CharField(max_length=255)
    males = models.IntegerField()
    females = models.IntegerField()
    total = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["year", "city_name", "school_code"],
                name="uniq_student_year_city_school",
            )
        ]

    def __str__(self):
        return f"{self.year} {self.school_name}"


class PopulationStat(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    city_name = models.CharField(max_length=64, db_index=True)
    county_code = models.CharField(max_length=32, blank=True)
    town_name = models.CharField(max_length=64)
    town_code = models.CharField(max_length=32)
    households = models.IntegerField()
    population = models.IntegerField()
    males = models.IntegerField()
    females = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["year", "month", "town_code"],
                name="uniq_population_period_town",
            )
        ]
        indexes = [
            models.Index(fields=["year", "month", "city_name"]),
        ]

    def __str__(self):
        return f"{self.year}-{self.month:02d} {self.town_name}"
