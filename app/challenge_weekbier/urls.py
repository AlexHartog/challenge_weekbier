
from django.urls import path
from django.contrib import admin

from . import views

app_name = 'challenge_weekbier'
urlpatterns = [
    # Home Page
    path('', views.new_checkin, name='home'),
    path('admin/', admin.site.urls),
    path('new_checkin', views.new_checkin, name='new_checkin'),
    path('standings', views.standings, name='standings'),
    path('checkins', views.checkins, name='checkins'),
    path('upload_csv', views.upload_csv, name='upload_csv'),
]