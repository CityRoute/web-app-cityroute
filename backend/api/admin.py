from django.contrib import admin
# from import_export import resources
from backend.api.models import Weather, Stop, FavouriteStop, Review, Route, RouteStop

# Register your models here.

admin.site.register(Weather)
admin.site.register(Stop)
admin.site.register(FavouriteStop)
admin.site.register(Route)
admin.site.register(Review)
admin.site.register(RouteStop)







# class StopResource(resources.ModelResource):
#     class Meta:
#         model = Stop