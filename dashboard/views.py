import json

from django.http import Http404
from django.shortcuts import render

from analysis.cities import CITY_SLUGS, SIX_CITIES, SLUG_BY_CITY
from analysis.income import income_totals_by_year, monthly_pci, per_100k_vehicles
from analysis.students import student_share, vehicle_share
from analysis.vehicles import ranking, totals_by_year

RANKING_META = {
    "all": {"title": "全國車輛數排行", "label": "車輛數"},
    "car": {"title": "全國小汽車數排行", "label": "小汽車數"},
    "scooter": {"title": "全國機車數排行", "label": "機車數"},
    "truck": {"title": "全國大貨車數排行", "label": "大貨車數"},
    "bus": {"title": "全國大客車數排行", "label": "大客車數"},
}

INCOME_META = {
    "all": {"title": "全部車輛", "label": "每10萬人均車數（輛）"},
    "car": {"title": "小汽車", "label": "每10萬人均小汽車數（輛）"},
    "scooter": {"title": "機車", "label": "每10萬人均機車數（輛）"},
}

STUDENT_META = {
    "car": {"title": "小汽車", "label": "小汽車於車輛中的比例"},
    "scooter": {"title": "機車", "label": "機車於車輛中的比例"},
}


def index(request):
    return render(request, "index.html")


def ranking_view(request, kind="all"):
    if kind not in RANKING_META:
        raise Http404()
    ranked, period = ranking(kind)
    meta = RANKING_META[kind]
    context = {
        "chart_title": meta["title"] if not period else f"{period[0]}年{period[1]}月｜{meta['title']}",
        "y_label": f"{meta['label']}（輛）",
        "city_names": json.dumps([row[0] for row in ranked], ensure_ascii=False),
        "values": json.dumps([row[1] for row in ranked]),
        "empty": not ranked,
    }
    return render(request, "charts/ranking.html", context)


def growth_view(request, city_slug=None):
    city_name = None
    region = "全國"
    if city_slug:
        city_name = CITY_SLUGS.get(city_slug)
        if not city_name:
            raise Http404()
        region = city_name
    income = income_totals_by_year(city_name=city_name)
    cap = max(income) if income else None
    vehicles = totals_by_year(city_name=city_name, up_to_year=cap)
    years = sorted(set(vehicles) | set(income))
    context = {
        "chart_title": f"{region}車輛數成長與家戶收入",
        "years": json.dumps(years),
        "vehicle_values": json.dumps([vehicles.get(year, 0) for year in years]),
        "income_values": json.dumps([income.get(year, 0) for year in years]),
        "region": region,
        "six_cities": [(SLUG_BY_CITY[name], name) for name in SIX_CITIES],
        "empty": not years,
    }
    return render(request, "charts/growth.html", context)


def income_view(request, kind="all"):
    if kind not in INCOME_META:
        raise Http404()
    vehicles, year = per_100k_vehicles(kind)
    pci, pci_year = monthly_pci()
    meta = INCOME_META[kind]
    context = {
        "chart_title": f"{year}年｜六都人均收入與{meta['title']}" if year else meta["title"],
        "vehicle_label": meta["label"],
        "city_names": json.dumps([row[0] for row in vehicles], ensure_ascii=False),
        "vehicle_values": json.dumps([row[1] for row in vehicles]),
        "income_values": json.dumps([row[1] for row in pci]),
        "empty": not vehicles or not pci,
        "year": year or pci_year,
    }
    return render(request, "charts/income.html", context)


def students_view(request, kind="car"):
    if kind not in STUDENT_META:
        raise Http404()
    vehicles, year = vehicle_share(kind)
    students, student_year = student_share()
    meta = STUDENT_META[kind]
    context = {
        "chart_title": f"{year}年｜六都學生比例與{meta['title']}" if year else meta["title"],
        "vehicle_label": meta["label"],
        "city_names": json.dumps([row[0] for row in vehicles], ensure_ascii=False),
        "vehicle_values": json.dumps([round(row[1] * 100, 2) for row in vehicles]),
        "student_values": json.dumps([round(row[1] * 100, 2) for row in students]),
        "empty": not vehicles or not students,
        "year": year or student_year,
    }
    return render(request, "charts/students.html", context)
