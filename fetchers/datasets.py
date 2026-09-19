from datetime import datetime

from django.conf import settings

from analysis.cities import TDX_CITIES
from dashboard.models import (
    City,
    HouseholdIncome,
    PopulationStat,
    StudentStatus,
    VehicleCount,
)
from fetchers.tdx import request_json


def seed_cities():
    for english, chinese in TDX_CITIES:
        City.objects.update_or_create(
            english_name=english,
            defaults={"chinese_name": chinese},
        )


def _cities():
    rows = list(City.objects.all())
    if rows:
        return rows
    seed_cities()
    return list(City.objects.all())


def fetch_vehicles(years=None):
    current = datetime.now().year
    years = years or range(current - 1, current + 1)
    stored = 0
    for year in years:
        for city in _cities():
            url = (
                f"{settings.TDX_API_BASE}/HouseholdVehicleOwnership/"
                f"Year/{year}/City/{city.english_name}?%24format=JSON"
            )
            payload = request_json(url)
            for result in payload.get("Results") or []:
                for month_data in result.get("VehicleData") or []:
                    month = month_data.get("Month")
                    for vehicle in month_data.get("Vehicles") or []:
                        VehicleCount.objects.update_or_create(
                            year=year,
                            month=month,
                            city_name=result.get("CityName") or city.chinese_name,
                            vehicle_type=vehicle.get("Type") or "",
                            defaults={
                                "county_code": result.get("CountyCode") or "",
                                "value": int(vehicle.get("Value") or 0),
                            },
                        )
                        stored += 1
    return stored


def fetch_income(years=None):
    current = datetime.now().year
    years = years or range(current - 1, current)
    stored = 0
    for year in years:
        for city in _cities():
            url = (
                f"{settings.TDX_API_BASE}/HouseholdIncome/"
                f"Year/{year}/City/{city.english_name}?%24format=JSON"
            )
            payload = request_json(url)
            for result in payload.get("Results") or []:
                household = result.get("Household") or {}
                HouseholdIncome.objects.update_or_create(
                    year=year,
                    city_name=result.get("CityName") or city.chinese_name,
                    defaults={
                        "county_code": result.get("CountyCode") or "",
                        "avg_households": float(household.get("AvgNumberOfHousehods") or 0),
                        "avg_employment": float(household.get("AvgNumberOfEmployment") or 0),
                        "avg_income_earners": float(household.get("AvgNumberOfIncome") or 0),
                        "total": float(household.get("Total") or 0),
                    },
                )
                stored += 1
    return stored


def fetch_students(years=None):
    current = datetime.now().year
    years = years or range(current - 1, current)
    stored = 0
    for year in years:
        for city in _cities():
            url = (
                f"{settings.TDX_API_BASE}/StudentStatus/"
                f"Year/{year}/City/{city.english_name}"
                f"?Type=%E5%A4%A7%E5%B0%88%E6%A0%A1%E9%99%A2&%24format=JSON"
            )
            payload = request_json(url)
            for result in payload.get("Results") or []:
                for school in result.get("Schools") or []:
                    for student in school.get("Students") or []:
                        StudentStatus.objects.update_or_create(
                            year=year,
                            city_name=result.get("CityName") or city.chinese_name,
                            school_code=student.get("SchoolCode") or "",
                            defaults={
                                "county_code": result.get("CountyCode") or "",
                                "school_type": school.get("Type") or "",
                                "school_name": student.get("SchoolName") or "",
                                "males": int(student.get("NumberOfMales") or 0),
                                "females": int(student.get("NumberOfFemales") or 0),
                                "total": int(student.get("Total") or 0),
                            },
                        )
                        stored += 1
    return stored


def fetch_population(years=None):
    current = datetime.now().year
    years = years or range(current - 1, current)
    stored = 0
    for year in years:
        for city in _cities():
            url = (
                f"{settings.TDX_API_BASE}/PopulationStats/"
                f"Year/{year}/City/{city.english_name}/Town?%24format=JSON"
            )
            payload = request_json(url)
            for result in payload.get("Results") or []:
                for month_data in result.get("TownData") or []:
                    month = int(month_data.get("Month") or 0)
                    for town in month_data.get("Towns") or []:
                        PopulationStat.objects.update_or_create(
                            year=year,
                            month=month,
                            town_code=town.get("TownCode") or "",
                            defaults={
                                "city_name": result.get("CityName") or city.chinese_name,
                                "county_code": result.get("CountyCode") or "",
                                "town_name": town.get("TownName") or "",
                                "households": int(town.get("NumberOfHousehods") or 0),
                                "population": int(town.get("NumberOfPopulation") or 0),
                                "males": int(town.get("NumberOfMales") or 0),
                                "females": int(town.get("NumberOfFemales") or 0),
                            },
                        )
                        stored += 1
    return stored
