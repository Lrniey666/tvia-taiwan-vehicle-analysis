from analysis.cities import SIX_CITIES
from analysis.vehicles import INCOME_VEHICLE_TYPES, six_city_totals
from dashboard.models import HouseholdIncome, PopulationStat


def latest_income_year():
    value = HouseholdIncome.objects.order_by("-year").values_list("year", flat=True).first()
    return value


def latest_population_period():
    latest = (
        PopulationStat.objects.order_by("-year", "-month")
        .values("year", "month")
        .first()
    )
    if not latest:
        return None
    return latest["year"], latest["month"]


def aligned_year():
    income_year = latest_income_year()
    pop = latest_population_period()
    if income_year is None or pop is None:
        return None
    return min(income_year, pop[0])


def income_totals_by_year(city_name=None):
    rows = HouseholdIncome.objects.all()
    if city_name:
        rows = rows.filter(city_name=city_name)
    totals = {}
    for row in rows:
        totals[row.year] = totals.get(row.year, 0) + row.total
    return dict(sorted(totals.items()))


def six_city_population(year, month, city_names=None):
    names = city_names or SIX_CITIES
    rows = PopulationStat.objects.filter(year=year, month=month, city_name__in=names)
    totals = {city: 0 for city in names}
    for row in rows:
        totals[row.city_name] += row.population
    return totals


def six_city_income_totals(year, city_names=None):
    names = city_names or SIX_CITIES
    rows = HouseholdIncome.objects.filter(year=year, city_name__in=names)
    totals = {city: 0.0 for city in names}
    for row in rows:
        totals[row.city_name] = row.total
    return totals


def per_100k_vehicles(kind="all"):
    year = aligned_year()
    pop_period = latest_population_period()
    if year is None or pop_period is None:
        return [], []
    types = INCOME_VEHICLE_TYPES[kind]
    vehicles = six_city_totals(year, 12, SIX_CITIES, types=types)
    population = six_city_population(year, pop_period[1])
    result = []
    for city, count in vehicles:
        people = population.get(city) or 0
        result.append([city, int(round(count / people * 100000)) if people else 0])
    return result, year


def monthly_pci():
    year = aligned_year()
    pop_period = latest_population_period()
    if year is None or pop_period is None:
        return [], None
    income = six_city_income_totals(year)
    population = six_city_population(year, pop_period[1])
    result = []
    for city in SIX_CITIES:
        people = population.get(city) or 0
        total = income.get(city) or 0
        result.append(
            [city, int(round(total * 1_000_000 / people / 12)) if people else 0]
        )
    return result, year
