from backend.api.models import Stop
from django.core.management.base import BaseCommand
# import os
import csv

# Use command to import csv file to Django model / populate table
class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        with open('backend/api/management/commands/stops.csv', encoding='UTF-8') as f:
            reader = csv.reader(f)
            total_count = 0
            fail_count = 0
            for row in reader:
                total_count += 1
                try:
                    created = Stop.objects.get_or_create(
                        unique_id= row[0],
                        name = row[1],
                        number = row[2],
                        latitude = row[3],
                        longitude = row[4]
                    )
                    
                    print("Imported", row[1], row[2])
                except:
                    print("Error on", row[1], row[2])
                    fail_count += 1
            print("Total:", total_count, "Fail:", fail_count)
        print('CSV imported to Django model.')