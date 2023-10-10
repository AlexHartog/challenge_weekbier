from django.contrib import admin
from django.urls import include, path

from . import views

app_name = "challenge_weekbier"
urlpatterns = [
    # Home Page
    path("", views.new_checkin, name="home"),
    path("admin/", admin.site.urls),
    path("new_checkin", views.new_checkin, name="new_checkin"),
    path("standings", views.standings, name="standings"),
    path("checkins", views.checkins, name="checkins"),
    path("upload_csv", views.upload_csv, name="upload_csv"),
    path("statistics", views.statistics, name="statistics"),
    path("filter_checkins/", views.filter_checkins, name="filter-checkins"),
    path("check_city/", views.check_city, name="check_city"),
    path("__reload__/", include("django_browser_reload.urls")),
]
