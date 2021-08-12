from django.test import TestCase
from backend.api.models import (Weather, User, Stop, FavouriteStop, 
                                Review, Route, RouteStop, FavouriteRoute, FavouriteDirections)

from datetime import datetime

class TestWeatherModel(TestCase):
    @classmethod
    def setUp(cls):
        Weather.objects.create(
            day_number = 1,
            datetime = "2021-09-12 12:00:00+00:00",
            temp_day = 30,
            temp_min = 10,
            temp_max = 30,
            temp_night = 5,
            temp_eve = 15,
            temp_morn = 10,
            windDirection = 5,
            windSpeed = 5,
            humidity = 5,
            pressure = 5,
            clouds = 5,
            precipitation = 5,
            weatherid = 5,
            rain = 5,
            main = "Rain", 
            description = "Rainy",
            scraped_on = "2021-08-12 12:00:00+00:00"
        )

        Stop.objects.create(
            number = 2,
            unique_id = "xxx",
            name = "Parnell square west",
            avg_dwelltime = 4.5,
            latitude = 3,
            longitude = 3
        )

        Route.objects.create(
            routeid = "46A"
        )

        RouteStop.objects.create(
            routeid = Route.objects.get(routeid='46A'),
            stopnumber = Stop.objects.get(number=2),
            outbound_yn = True,
            order = 1,
            percent_of_route = 100
        )

    def test_weather_max_length(self):
        weather = Weather.objects.get(day_number=1)
        max_length = weather._meta.get_field("main").max_length
        self.assertEquals(max_length, 20)

        max_length = weather._meta.get_field("description").max_length
        self.assertEquals(max_length, 50)

    def test_stop_max_length(self):
        stop = Stop.objects.get(number=2)
        max_length = stop._meta.get_field("unique_id").max_length
        self.assertEquals(max_length, 15)

        max_length = stop._meta.get_field("name").max_length
        self.assertEquals(max_length, 50)

    def test_route_max_length(self):
        route = Route.objects.get(routeid="46A")
        max_length = route._meta.get_field("routeid").max_length
        self.assertEquals(max_length, 20)    

    def test_route_stop_matches(self):
        """ Checking the joining table RouteStop is properly connected """

        route = Route.objects.get(routeid='46A')
        stop = Stop.objects.get(number=2)
        routestop_byroute = RouteStop.objects.get(routeid=route)
        routestop_bystop = RouteStop.objects.get(stopnumber=stop)
        self.assertEquals(routestop_byroute, routestop_bystop)


class TestFavouriteModels(TestCase):
    @classmethod
    def setUp(cls):
        User.objects.create(
            username='johnsmith',
            password='password',
            email='john@email.com',
            first_name='John',
            last_name='Smith'

        )
        
        Stop.objects.create(
            number = 2,
            unique_id = "xxx",
            name = "Parnell square west",
            avg_dwelltime = 4.5,
            latitude = 3,
            longitude = 3
        )

        FavouriteStop.objects.create(
            user=User.objects.get(id=1),
            stopid = Stop.objects.get(number=2)

        )

        Route.objects.create(
            routeid = "46A"
        )

        FavouriteRoute.objects.create(
            user=User.objects.get(id=1),
            routeid=Route.objects.get(routeid='46A')

        )

        FavouriteDirections.objects.create(
            directions_id=3,
            user=User.objects.get(id=1),
            origin="Urban Outfitters, Cecilia Street, Temple Bar, Dublin 2, Ireland",
            destination="UCD O'Reilly Hall, Belfield, Dublin, Ireland",
            url="xxx"

        )

    def test_users_fav_stop_matches(self):
        user = User.objects.get(id=1)
        users_favourite_stop = FavouriteStop.objects.get(user=user).stopid
        stop = Stop.objects.get(number=2)
        self.assertEquals(stop, users_favourite_stop)


    def test_users_fav_route_matches(self):
        user = User.objects.get(id=1)
        users_favourite_route = FavouriteRoute.objects.get(user=user).routeid
        route = Route.objects.get(routeid='46A')
        self.assertEquals(route, users_favourite_route)

    def test_users_fav_journey_matches(self):
        user = User.objects.get(id=1)
        users_favourite_journey = FavouriteDirections.objects.get(user=user)
        journey = FavouriteDirections.objects.get(directions_id=3)
        self.assertEquals(journey, users_favourite_journey)

    
    def test_unique_together_favstop(self):
        # Attempt to create an identical object of FavouriteStop
        with self.assertRaises(Exception):
            original_clone = FavouriteStop.objects.create(
                user=User.objects.get(id=1),
                stopid = Stop.objects.get(number=2)
            )

    def test_unique_together_favroute(self):
        with self.assertRaises(Exception):
            original_clone = FavouriteRoute.objects.create(
                user=User.objects.get(id=1),
                routeid=Route.objects.get(routeid='46A')
            )

    def test_unique_together_favdirections(self):
        with self.assertRaises(Exception):
            original_clone = FavouriteDirections.objects.create(
                directions_id=3,
                user=User.objects.get(id=1),
                origin="Urban Outfitters, Cecilia Street, Temple Bar, Dublin 2, Ireland",
                destination="UCD O'Reilly Hall, Belfield, Dublin, Ireland",
                url="xxx"
            )