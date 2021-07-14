from django.contrib import admin
from import_export import resources
from backend.api.models import Stop
from backend.api.models import Weather

# Register your models here.
admin.site.register(Weather)
admin.site.register(Stop)

class StopResource(resources.ModelResource):
    class Meta:
        model = Stop