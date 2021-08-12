from django.test import TestCase, Client
from django.urls import reverse
from backend.api.models import Weather, User, Stop, FavouriteStop, Review, Route, FavouriteRoute, FavouriteDirections
import json

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        