"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .api.views import (
    index_view,
    MessageViewSet,
    BusStopTimes,
    RegisterApi,
    ChangePasswordView,
    WeatherByDay,
)

router = routers.DefaultRouter()
router.register("messages", MessageViewSet)

urlpatterns = [
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
    path("api/change-password/", ChangePasswordView.as_view(), name="change-password"),
    path(
        "api/password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
    # http://localhost:8000/api/weather/<day>
    path(
        "api/weather-forecast/<int:day_number>", WeatherByDay, name="weather-forecast"
    ),
]
