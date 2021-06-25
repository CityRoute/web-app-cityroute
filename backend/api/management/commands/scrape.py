from django.core.management.base import BaseCommand
import urllib3
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
from backend.api.models import Weather
import requests
import psycopg2

conn = psycopg2.connect(database="users", user="stephanie", password="password", host="", port="")
cur = conn.cursor()

api_url = "api.openweathermap.org/data/2.5/forecast/daily?q=Dublin"
appid = "595c29ce82ae35b1caa367d86f0a8b26"




class Command(BaseCommand):
    help = "collect weather data"
    # define logic of command
    def handle(self, *args, **options):
        global weatherForecastResult
        weatherForecastResult = requests.get(api_url, params={"appid":appid, "units": "metric"})
        data = json.loads(weatherForecastResult.text)

        # # collect html
        # html = urlopen('https://jobs.lever.co/opencare')
        # # convert to soup
        # soup = BeautifulSoup(html, 'html.parser')
        # # grab all postings
        # postings = soup.find_all("div", class_="posting")
        # for p in postings:
        #     url = p.find('a', class_='posting-btn-submit')['href']
        #     title = p.find('h5').text
        #     location = p.find('span', class_='sort-by-location').text
        #     # check if url in db
        #     try:
        #         # save in db
        #         Weather.objects.create(
        #             url=url,
        #             title=title,
        #             location=location
        #         )
        #         print('%s added' % (title,))
        #     except:
        #         print('%s already exists' % (title,))
        # self.stdout.write( 'job complete' )