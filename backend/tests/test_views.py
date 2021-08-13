from django.test import TestCase, Client
from django.urls import reverse
from backend.api.models import Weather, User, Stop, FavouriteStop, Review, Route, FavouriteRoute, FavouriteDirections, RouteStop
import json
from backend.api.views import (index_view, BusStopTimes, RegisterApi,
                        ChangePasswordView, WeatherByDay, GetAllReviews,
                        writeReview, GetRouteStops, addFavRoute,
                        FavouriteRoutes, addFavDirections,
                        GetFavouriteDirections, WeatherByDay, FavouriteStopsAll, 
                        FavouriteStops, addFavStop, getAllStops, GetAllRoutes)
from backend.api.machine_learning.views import ModelPredictionView
from backend.api.serializer import RegisterSerializer, UserSerializer, WeatherSerializer, StopSerializer, FavouriteStopSerializer, RouteSerializer, ReviewSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        # URLs/Views
        self.getallstops_url = reverse("stops-all")
        self.getallreviews_url = reverse("reviews-all")
        self.getallroutes_url = reverse("routes-all")
        self.getallroutestops_url = reverse("route-stops")
        self.getfavstops_url = reverse("favourite-stops")

        Stop.objects.create(
            number = 1,
            unique_id = 'xxx',
            name = 'Test Stop 1',
            avg_dwelltime= 1,
            latitude=1,
            longitude=1

        )
        Stop.objects.create(
            number = 2,
            unique_id = 'xxy',
            name = 'Test Stop 2',
            avg_dwelltime= 1,
            latitude=1,
            longitude=1

        )

        User.objects.create(
            username='johnsmith',
            password='password',
            email='john@email.com',
            first_name='John',
            last_name='Smith'

        )

        Route.objects.create(
            routeid = '46A'
        )

        Review.objects.create(
            user = User.objects.get(username='johnsmith'),
            content = 'blabla',
            clean_rating = 1,
            speed_rating = 1,
            accuracy_rating = 1,
            routeid = Route.objects.get(routeid='46A')
        )

        RouteStop.objects.create(
            routeid = Route.objects.get(routeid='46A'),
            stopnumber = Stop.objects.get(number=2),
            outbound_yn = True,
            order = 1,
            percent_of_route = 100
        )

        FavouriteStop.objects.create(
            user = User.objects.get(username='johnsmith'),
            stopid = Stop.objects.get(unique_id='xxx')
        )

        FavouriteRoute.objects.create(
            user = User.objects.get(username='johnsmith'),
            routeid = Route.objects.get(routeid='46A')
        )

        FavouriteDirections.objects.create(
            directions_id = 1,
            user = User.objects.get(username='johnsmith'),
            origin="Urban Outfitters, Cecilia Street, Temple Bar, Dublin 2, Ireland",
            destination="UCD O'Reilly Hall, Belfield, Dublin, Ireland",
            url="xxx"
        )

    def test_get_all_stops_returns_correct_stops(self):
        response = self.client.get(self.getallstops_url)
        stops = Stop.objects.all()
        serializer = StopSerializer(stops, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_get_all_stops_returns_correct_stops(self):
    #     pass



    # def test_get_all_reviews_returns_correct_number_of_reviews(self):
    #     response = self.client.get(self.getallreviews_url)
    #     self.assertEqual(response.status_code, 200)

    def test_get_all_reviews_returns_correct_reviews(self):
        response = self.client.get(self.getallreviews_url)
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_routes_returns_correct_routes(self):
        response = self.client.get(self.getallroutes_url)
        routes = Route.objects.all()
        serializer = RouteSerializer(routes, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_get_all_routestops_returns_correct_routestops(self):
    #     response = self.client.get(self.getallroutestops_url)
    #     routestops = RouteStop.objects.all()
    #     serializer = StopSerializer(routestops, many=True)
    #     self.assertEqual(response.data, serializer.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_get_favourite_stops_returns_correct_stops(self):
    #     response = self.client.get(self.getfavstops_url)
    #     user = User.objects.get(username='johnsmith')
    #     favstops = FavouriteStop.objects.get(user=user)
    #     self.assertEqual(response.data, favstops.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)