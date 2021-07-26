from django.contrib import admin
# from import_export import resources
from backend.api.models import Weather, Stop, User, FavouriteStop, Review

# Register your models here.

admin.site.register(Weather)
admin.site.register(Stop)
admin.site.register(FavouriteStop)
admin.site.register(Review)







# class StopResource(resources.ModelResource):
#     class Meta:
#         model = Stop