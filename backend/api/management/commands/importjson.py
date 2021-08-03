from django.core.management.base import BaseCommand

from backend.api.models import Route
import json

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        
        with open('backend/api/management/commands/routes_and_stops.json') as f:
            reader = json.load(f)
            print()
            for key, value in reader.items():
                for k,v in value.items():
                    if k == "inbound":
                        inbound = list(map(int, v))
                    elif k == "outbound":
                        outbound = list(map(int, v))
                print(key, type(inbound), type(outbound))

                Route.objects.create(
                    id = key,
                    stops_outbound = outbound, 
                    stops_inbound = inbound
                )
                   

                   
               
        print('JSON imported to Django model.')