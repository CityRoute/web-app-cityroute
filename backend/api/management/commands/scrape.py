from django.core.management.base import BaseCommand
import json
from backend.api.models import Weather
# import psycopg2
from datetime import datetime
from django.utils.timezone import make_aware, now
import time
import requests

import os

class Command(BaseCommand):
    appid = os.getenv("weatherapikey")
    api_url = "http://api.openweathermap.org/data/2.5/forecast/daily?q=Dublin,IE&cnt=16&units=metric&cnt=16&appid={id}".format(id = appid)
    
    # define logic of command
    def handle(self, *args, **options):

        global weatherForecastResult
        weatherForecastResult = requests.get(self.api_url, params={"appid":self.appid, "units": "metric"})
        data = json.loads(weatherForecastResult.text)
        days = data.get("list")

        try:
            number = 1 # for incrementing day_number
            for day in days:
                # save in db
                unix_timestamp = day["dt"]
                timestamp = make_aware(datetime.fromtimestamp(unix_timestamp))
                today = make_aware(datetime.fromtimestamp(time.time()))
                
                w = Weather(
                    day_number = number, 
                    datetime = timestamp,
                    temp_day = day["temp"]["day"],
                    temp_min = day["temp"]["min"],
                    temp_max = day["temp"]["max"],
                    temp_night = day["temp"]["night"],
                    temp_eve = day["temp"]["eve"],
                    temp_morn = day["temp"]["morn"],
                    windDirection = day["deg"],
                    windSpeed = day["speed"],
                    humidity = day["humidity"],
                    pressure = day["pressure"],
                    clouds = day["clouds"],
                    precipitation = day["pop"], # probability of precipiation
                    weatherid = day["weather"][0]["id"],
                    rain = 0,
                    main = day["weather"][0]["main"],
                    scraped_on = today # PK
                )

                if "rain" in day:
                    w.rain = day["rain"]
                
                w.save()
                
        
                number += 1 
            print('Scraping job complete!')
        except:
            print("An error occurred - entries not added to table")


