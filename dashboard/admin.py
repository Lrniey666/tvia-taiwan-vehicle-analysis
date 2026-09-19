from django.contrib import admin

from .models import City, HouseholdIncome, PopulationStat, StudentStatus, VehicleCount


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("chinese_name", "english_name")
    search_fields = ("chinese_name", "english_name")


@admin.register(VehicleCount)
class VehicleCountAdmin(admin.ModelAdmin):
    list_display = ("year", "month", "city_name", "vehicle_type", "value")
    list_filter = ("year", "vehicle_type", "city_name")


@admin.register(HouseholdIncome)
class HouseholdIncomeAdmin(admin.ModelAdmin):
    list_display = ("year", "city_name", "total")
    list_filter = ("year",)


@admin.register(StudentStatus)
class StudentStatusAdmin(admin.ModelAdmin):
    list_display = ("year", "city_name", "school_name", "total")
    search_fields = ("school_name",)


@admin.register(PopulationStat)
class PopulationStatAdmin(admin.ModelAdmin):
    list_display = ("year", "month", "city_name", "town_name", "population")
    list_filter = ("year", "city_name")
