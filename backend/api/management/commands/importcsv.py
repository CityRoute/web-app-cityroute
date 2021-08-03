from backend.api.models import Stop
from django.core.management.base import BaseCommand
# import os
import csv

# Use command to import csv file to Django model / populate table
class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        with open('backend/api/management/commands/stops.csv', encoding='UTF-8') as f:
            reader = csv.reader(f)
            for row in reader:
                created = Stop.objects.get_or_create(
                    unique_id= row[0],
                    name = row[1],
                    number = row[2],
                    latitude = row[3],
                    longitude = row[4]
                )
        print('CSV imported to Django model.')