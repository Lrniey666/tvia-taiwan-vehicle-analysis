from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("rankings/", views.ranking_view, {"kind": "all"}, name="ranking"),
    path("rankings/<str:kind>/", views.ranking_view, name="ranking_kind"),
    path("growth/", views.growth_view, name="growth"),
    path("growth/<slug:city_slug>/", views.growth_view, name="growth_city"),
    path("income/", views.income_view, {"kind": "all"}, name="income"),
    path("income/<str:kind>/", views.income_view, name="income_kind"),
    path("students/", views.students_view, {"kind": "car"}, name="students"),
    path("students/<str:kind>/", views.students_view, name="students_kind"),
]
