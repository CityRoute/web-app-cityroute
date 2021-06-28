from django.contrib import admin

# Register your models here.

from backend.api.models import Weather
admin.site.register(Weather)