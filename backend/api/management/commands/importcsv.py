from backend.api.models import Stop
from django.core.management.base import BaseCommand
import os
import csv

from backend.settings.dev import BASE_DIR

# Use command to import csv file to Django model / populate table
class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        with open('backend/api/management/commands/stops.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                created = Stop.objects.get_or_create(
                    unique_id= row[0],
                    name = row[1],
                    latitude = row[2],
                    longitude = row[3]
                )