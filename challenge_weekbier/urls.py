"""Defines the URL patterns for learning logs."""

from django.urls import path

from . import views

app_name = 'challenge_weekbier'

urlpatterns = [
    # Home Page
    path('', views.home, name='home'),
    path('new_checkin', views.new_checkin, name='new_checkin'),
]
