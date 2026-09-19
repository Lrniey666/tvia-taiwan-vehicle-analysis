"""Build a secret-free Django fixture from the 2023 sqlite dump. Read-only on the source."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "original-data" / "python-10" / "db.sqlite3"
DEST = ROOT / "data" / "fixtures" / "demo.json"

CITIES = [
    ("Taipei", "臺北市"),
    ("NewTaipei", "新北市"),
    ("Taoyuan", "桃園市"),
    ("Taichung", "臺中市"),
    ("Tainan", "臺南市"),
    ("Kaohsiung", "高雄市"),
    ("Keelung", "基隆市"),
    ("Hsinchu", "新竹市"),
    ("HsinchuCounty", "新竹縣"),
    ("MiaoliCounty", "苗栗縣"),
    ("ChanghuaCounty", "彰化縣"),
    ("NantouCounty", "南投縣"),
    ("YunlinCounty", "雲林縣"),
    ("Chiayi", "嘉義市"),
    ("ChiayiCounty", "嘉義縣"),
    ("PingtungCounty", "屏東縣"),
    ("YilanCounty", "宜蘭縣"),
    ("HualienCounty", "花蓮縣"),
    ("TaitungCounty", "臺東縣"),
    ("PenghuCounty", "澎湖縣"),
    ("KinmenCounty", "金門縣"),
    ("LienchiangCounty", "連江縣"),
]


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


def main():
    if not SOURCE.exists():
        raise SystemExit(f"missing {SOURCE}")

    conn = sqlite3.connect(SOURCE)
    conn.row_factory = sqlite3.Row
    records = []

    for pk, (english, chinese) in enumerate(CITIES, start=1):
        records.append(
            {
                "model": "dashboard.city",
                "pk": pk,
                "fields": {"english_name": english, "chinese_name": chinese},
            }
        )

    seen_vehicle = {}
    for row in conn.execute("SELECT * FROM mysite_vehicle"):
        key = (_int(row["year"]), _int(row["month"]), row["city_name"], row["vehicle_type"])
        seen_vehicle[key] = {
            "year": key[0],
            "month": key[1],
            "city_name": row["city_name"],
            "county_code": row["county_code"] or "",
            "vehicle_type": row["vehicle_type"],
            "value": _int(row["value"]),
        }
    for pk, fields in enumerate(seen_vehicle.values(), start=1):
        records.append({"model": "dashboard.vehiclecount", "pk": pk, "fields": fields})

    seen_income = {}
    for row in conn.execute("SELECT * FROM mysite_household_income"):
        key = (_int(row["year"]), row["city_name"])
        seen_income[key] = {
            "year": key[0],
            "city_name": row["city_name"],
            "county_code": row["county_code"] or "",
            "avg_households": _float(row["Avg_number_of_househods"]),
            "avg_employment": _float(row["Avg_number_of_employment"]),
            "avg_income_earners": _float(row["Avg_number_of_income"]),
            "total": _float(row["Total"]),
        }
    for pk, fields in enumerate(seen_income.values(), start=1):
        records.append({"model": "dashboard.householdincome", "pk": pk, "fields": fields})

    seen_students = {}
    for row in conn.execute("SELECT * FROM mysite_universities_and_colleges_student_status"):
        key = (_int(row["year"]), row["city_name"], row["SchoolCode"] or "")
        seen_students[key] = {
            "year": key[0],
            "city_name": row["city_name"],
            "county_code": row["county_code"] or "",
            "school_type": row["type"] or "",
            "school_code": row["SchoolCode"] or "",
            "school_name": row["SchoolName"] or "",
            "males": _int(row["NumberOfMales"]),
            "females": _int(row["NumberOfFemales"]),
            "total": _int(row["Total"]),
        }
    for pk, fields in enumerate(seen_students.values(), start=1):
        records.append({"model": "dashboard.studentstatus", "pk": pk, "fields": fields})

    seen_pop = {}
    for row in conn.execute("SELECT * FROM mysite_population_stats"):
        key = (_int(row["Year"]), _int(row["Month"]), row["TownCode"] or "")
        seen_pop[key] = {
            "year": key[0],
            "month": key[1],
            "city_name": row["CityName"],
            "county_code": row["CountyCode"] or "",
            "town_name": row["TownName"] or "",
            "town_code": row["TownCode"] or "",
            "households": _int(row["NumberOfHousehods"]),
            "population": _int(row["NumberOfPopulation"]),
            "males": _int(row["NumberOfMales"]),
            "females": _int(row["NumberOfFemales"]),
        }
    for pk, fields in enumerate(seen_pop.values(), start=1):
        records.append({"model": "dashboard.populationstat", "pk": pk, "fields": fields})

    conn.close()
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_text(json.dumps(records, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {len(records)} objects to {DEST}")


if __name__ == "__main__":
    main()
