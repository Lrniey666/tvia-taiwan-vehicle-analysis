from dashboard.models import VehicleCount

RANKING_TYPES = {
    "all": None,
    "car": ["小客車"],
    "scooter": ["機車"],
    "truck": ["大貨車"],
    "bus": ["大客車"],
}

INCOME_VEHICLE_TYPES = {
    "all": None,
    "car": ["小客車", "小貨車"],
    "scooter": ["機車"],
}


def latest_vehicle_period():
    latest = (
        VehicleCount.objects.order_by("-year", "-month").values("year", "month").first()
    )
    if not latest:
        return None
    return latest["year"], latest["month"]


def ranking(kind="all"):
    period = latest_vehicle_period()
    if not period:
        return [], None
    year, month = period
    rows = VehicleCount.objects.filter(year=year, month=month)
    types = RANKING_TYPES[kind]
    totals = {}
    for row in rows:
        if types is not None and row.vehicle_type not in types:
            continue
        totals[row.city_name] = totals.get(row.city_name, 0) + row.value
    ranked = sorted(totals.items(), key=lambda item: item[1], reverse=True)
    return ranked, (year, month)


def totals_by_year(city_name=None, up_to_year=None, month=12):
    rows = VehicleCount.objects.filter(month=month)
    if city_name:
        rows = rows.filter(city_name=city_name)
    if up_to_year is not None:
        rows = rows.filter(year__gte=2016, year__lte=up_to_year)
    totals = {}
    for row in rows:
        totals[row.year] = totals.get(row.year, 0) + row.value
    return dict(sorted(totals.items()))


def six_city_totals(year, month, city_names, types=None):
    rows = VehicleCount.objects.filter(year=year, month=month, city_name__in=city_names)
    totals = {city: 0 for city in city_names}
    for row in rows:
        if types is not None and row.vehicle_type not in types:
            continue
        totals[row.city_name] += row.value
    return [[city, totals[city]] for city in city_names]
