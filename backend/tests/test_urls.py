from django.test import SimpleTestCase
from django.urls import reverse, resolve
from backend.api.views import (index_view, BusStopTimes, RegisterApi,
                        ChangePasswordView, WeatherByDay, GetAllReviews,
                        writeReview, GetRouteStops, addFavRoute,
                        FavouriteRoutes, addFavDirections,
                        GetFavouriteDirections, WeatherByDay, FavouriteStopsAll, 
                        FavouriteStops, addFavStop, getAllStops, GetAllRoutes)
from backend.api.machine_learning.views import ModelPredictionView


class TestUrls(SimpleTestCase):

    def test_index_view(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func, index_view)

    # def test_get_bus_stop_times(self):
    #     bus_stop = 2
    #     url = reverse('bus-stop-times', args=(bus_stop,))

    def test_get_all_stops(self):
        url = reverse('stops-all')
        self.assertEquals(resolve(url).func, getAllStops)

    def test_get_weather_forecast(self):
        day_number = 1
        url = reverse('weather-forecast', args=(day_number,))
        self.assertEquals(resolve(url).func, WeatherByDay)

    def test_get_all_routes(self):
        url = reverse('routes-all')
        self.assertEquals(resolve(url).func, GetAllRoutes)

    def test_get_route_stops(self):
        url = reverse('route-stops')
        self.assertEquals(resolve(url).func, GetRouteStops)

    def test_get_all_reviews(self):
        url = reverse('reviews-all')
        self.assertEquals(resolve(url).func, GetAllReviews)

    def test_write_review(self):
        url = reverse('write-review')
        self.assertEquals(resolve(url).func, writeReview)

    def test_get_all_favourite_stops(self):
        url = reverse('favourite-stops-all')
        self.assertEquals(resolve(url).func, FavouriteStopsAll)

    def test_get_favourite_stops(self):
        url = reverse('favourite-stops')
        self.assertEquals(resolve(url).func, FavouriteStops)

    def test_get_favourite_routes(self):
        url = reverse('favourite-routes')
        self.assertEquals(resolve(url).func, FavouriteRoutes)
    
    def test_get_favourite_directions(self):
        url = reverse('favourite-directions')
        self.assertEquals(resolve(url).func, GetFavouriteDirections)

    def test_add_favourite_route(self):
        url = reverse('add-favourite-route')
        self.assertEquals(resolve(url).func, addFavRoute)

    def test_add_favourite_stop(self):
        number = 11
        url = reverse('add-favourite-stops', args=(number,))
        self.assertEquals(resolve(url).func, addFavStop)

    def test_get_model_prediction(self):
        url = reverse('model-prediction')
        self.assertEquals(resolve(url).func, ModelPredictionView)