from analysis.cities import SIX_CITIES
from analysis.vehicles import six_city_totals
from dashboard.models import PopulationStat, StudentStatus


def latest_student_year():
    return StudentStatus.objects.order_by("-year").values_list("year", flat=True).first()


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
    students = latest_student_year()
    pop = latest_population_period()
    if students is None or pop is None:
        return None
    return min(students, pop[0])


def six_city_students(year):
    rows = StudentStatus.objects.filter(year=year, city_name__in=SIX_CITIES)
    totals = {city: 0 for city in SIX_CITIES}
    for row in rows:
        totals[row.city_name] += row.total
    return totals


def six_city_population(year, month):
    rows = PopulationStat.objects.filter(
        year=year, month=month, city_name__in=SIX_CITIES
    )
    totals = {city: 0 for city in SIX_CITIES}
    for row in rows:
        totals[row.city_name] += row.population
    return totals


def student_share():
    year = aligned_year()
    pop_period = latest_population_period()
    if year is None or pop_period is None:
        return [], None
    students = six_city_students(year)
    population = six_city_population(year, pop_period[1])
    result = []
    for city in SIX_CITIES:
        people = population.get(city) or 0
        result.append([city, round(students[city] / people, 4) if people else 0])
    return result, year


def vehicle_share(kind):
    year = aligned_year()
    pop_period = latest_population_period()
    if year is None or pop_period is None:
        return [], None
    month = pop_period[1]
    types = ["小客車"] if kind == "car" else ["機車"]
    subset = six_city_totals(year, month, SIX_CITIES, types=types)
    all_vehicles = six_city_totals(year, month, SIX_CITIES, types=None)
    all_map = {city: value for city, value in all_vehicles}
    result = []
    for city, count in subset:
        total = all_map.get(city) or 0
        result.append([city, round(count / total, 4) if total else 0])
    return result, year
