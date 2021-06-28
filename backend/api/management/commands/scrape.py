from django.core.management.base import BaseCommand
import json
from backend.api.models import Weather
import requests
import psycopg2
from datetime import datetime
import time
from django.utils.timezone import make_aware, now


import os

class Command(BaseCommand):
    appid = os.getenv("weatherapikey")
    api_url = "http://api.openweathermap.org/data/2.5/forecast/daily?q=Dublin&cnt=16&appid={id}".format(id = appid)
    
    # define logic of command
    def handle(self, *args, **options):
        global weatherForecastResult
        weatherForecastResult = requests.get(self.api_url, params={"appid":self.appid, "units": "metric"})
        data = json.loads(weatherForecastResult.text)
        days = data.get("list")

        for day in days:
            # save in db
            unix_timestamp = day["dt"]
            timestamp = make_aware(datetime.fromtimestamp(unix_timestamp))
            Weather.objects.create(
                # lon = 
                # lat = 
                datetime = timestamp,
                temperature = day["temp"]["day"],
                windDirection = day["deg"],
                windSpeed = day["speed"],
                humidity = day["humidity"],
                pressure = day["pressure"],
                clouds = day["clouds"],
                precipitation = day["pop"], # probability of precipiation
                weatherid = day["weather"][0]["id"],
                # created_date = now
            )

                # print('Weather at datetime {} added'.format(datetime))
            # except:
            #     print("error occurred - entry not added to table")
        self.stdout.write( 'scraping job complete' )


