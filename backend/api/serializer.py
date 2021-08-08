from rest_framework import  serializers
from rest_framework.permissions import IsAuthenticated
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from .models import Weather, FavouriteStop, User, Stop, Route, Review
# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','password','first_name', 'last_name', 'email')
        extra_kwargs = {
            'password':{'write_only': True},
        }
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],     password = validated_data['password']  ,first_name=validated_data['first_name'],  last_name=validated_data['last_name'], email=validated_data['email'])
        return user
# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class CustomTokenSerializer(serializers.Serializer):
    token = serializers.CharField()


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = '__all__'

class StopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stop
        fields = '__all__'


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'


class FavouriteStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteStop
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'