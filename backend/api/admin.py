from django.contrib import admin
from import_export import resources
from backend.api.models import Weather, Stop, User, FavouriteStop

# Register your models here.

admin.site.unregister(User)
admin.site.register(User)

admin.site.register(Weather)
admin.site.register(Stop)
admin.site.register(FavouriteStop)






class StopResource(resources.ModelResource):
    class Meta:
        model = Stop