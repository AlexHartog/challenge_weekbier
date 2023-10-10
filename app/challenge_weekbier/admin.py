from django.contrib import admin

from .models import Checkin, Player

admin.site.register(Player)
admin.site.register(Checkin)
