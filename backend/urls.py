"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
"""

from backend.api.serializer import FavouriteStopSerializer
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .api.views import (index_view, BusStopTimes, RegisterApi,
                        ChangePasswordView, WeatherByDay, GetAllReviews,
                        writeReview, GetRouteStops, addFavRoute, deleteFavStop,
                        deleteFavRoute, deleteFavDirections, FavouriteRoutes,
                        addFavDirections, GetFavouriteDirections)
from .api.views import index_view, BusStopTimes, RegisterApi, ChangePasswordView, WeatherByDay, FavouriteStopsAll, FavouriteStops, addFavStop, getAllStops, GetAllRoutes
from .api.machine_learning.views import ModelPredictionView

router = routers.DefaultRouter()
app_name = 'smth'

urlpatterns = [
    path('api/admin/', admin.site.urls),
    url('api-token/', TokenObtainPairView.as_view()),
    url('api-token-refresh/', TokenRefreshView.as_view()),
    path('api/register', RegisterApi.as_view()),
    path('api/change-password/',
         ChangePasswordView.as_view(),
         name='change-password'),
    path('api/password_reset/',
         include('django_rest_passwordreset.urls',
                 namespace='password_reset')),

    # http://localhost:8000/
    path("", index_view, name="index"),
    path("api/bus-stop-times/<int:bus_stop>", BusStopTimes),

    # http://localhost:8000/api/<router-viewsets>
    path("api/", include(router.urls)),

    # http://localhost:8000/api/admin/
    path("api/admin/", admin.site.urls),
    url("api-token/", TokenObtainPairView.as_view()),
    url("api-token-refresh/", TokenRefreshView.as_view()),
    path("api/register", RegisterApi.as_view()),
    path("api/change-password/",
         ChangePasswordView.as_view(),
         name="change-password"),
    path(
        "api/password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
    # http://localhost:8000/api/weather/<day>
    path("api/weather-forecast/<int:day_number>",
         WeatherByDay,
         name="weather-forecast"),

    # http://localhost:8000/api/weather-forecast/<day>
    path('api/weather-forecast/<int:day_number>',
         WeatherByDay,
         name='weather-forecast'),

    # http://localhost:8000/api/stops-all/
    path('api/stops-all/', getAllStops, name='stops-all'),
    path('api/routes-all/', GetAllRoutes, name='routes-all'),
    path('api/route-stops/', GetRouteStops, name='routes-all'),
    path('api/reviews-all/', GetAllReviews, name='reviews-all'),
    path('api/write-review/', writeReview, name='write-review'),

    # http://localhost:8000/api/favourite-stops-all/
    path('api/favourite-stops-all/',
         FavouriteStopsAll,
         name='favourite-stops-all'),
    # http://localhost:8000/api/favourite-stops/
    path('api/favourite-routes/', FavouriteRoutes, name='favourite-routes'),

    # http://localhost:8000/api/add-fav-stop/<number>
    path('api/add-fav-route/', addFavRoute, name='add-favourite-route'),
    # http://localhost:8000/api/favourite-stops/
    path('api/favourite-stops/', FavouriteStops, name='favourite-stops'),
    path('api/add-fav-directions/',
         addFavDirections,
         name='add-favourite-directions'),
    # http://localhost:8000/api/favourite-stops/
    path('api/favourite-directions/',
         GetFavouriteDirections,
         name='favourite-directions'),

    # http://localhost:8000/api/add-fav-stop/<number>
    path('api/add-fav-stop/<int:number>',
         addFavStop,
         name='add-favourite-stops'),
    path('api/delete-fav-stop/<int:number>',
         deleteFavStop,
         name='delete-favourite-stops'),
    path('api/delete-fav-route/<int:number>',
         deleteFavRoute,
         name='delete-favourite-routes'),
    path('api/delete-fav-directions/<int:number>',
         deleteFavDirections,
         name='delete-favourite-directions'),
    path('api/model-prediction/', ModelPredictionView,
         name='model-prediction'),
]
