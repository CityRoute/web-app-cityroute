from django.core.management.base import BaseCommand

from backend.api.models import Route, RouteStop, Stop
import json

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        
        with open('backend/api/management/commands/stop_dwelltimes.json') as f:
            stops = json.load(f)
        
        fail_count = 0
        total_count = 0
        for stop_number, dwelltime in stops.items():
            print(f"stop number: {stop_number}")
            try:
                s = Stop.objects.get(number=stop_number)
                s.avg_dwelltime = dwelltime
                s.save()
            except Exception as e:
                fail_count += 1

            total_count += 1
        
        print(f"total: {total_count}, fail: {fail_count}")
        
            