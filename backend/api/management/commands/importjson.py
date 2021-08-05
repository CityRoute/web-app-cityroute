from django.core.management.base import BaseCommand

from backend.api.models import Route, RouteStop, Stop
import json

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        
        with open('backend/api/management/commands/routes_and_stops.json') as f:
            routes = json.load(f)
            print()
            for route_num, stop_list in routes.items():
                print(f"route number: {route_num}")
                try:
                    Route.objects.create(
                        routeid = route_num)
                except:
                    pass
                # print(id)
                exit
                for stop_direction, stop_num_list in stop_list.items():
                    total_count = 0
                    fail_count = 0
                    order = 0
                    for stop_num in stop_num_list:
                        total_count += 1
                        print(f"stop number: {stop_num}")
                        
                        try:
                            route = Route.objects.get(pk=route_num)
                            stopnumber = Stop.objects.get(number=stop_num)
                            RouteStop.objects.create(
                                routeid = route,
                                stopnumber = stopnumber,
                                outbound_yn = True if stop_direction == 'outbound' else False,
                                order=order)
                            order += 1
                        except Exception as e:
                            print(e)
                            fail_count += 1
                            pass
                print(f"total: {total_count}, fail: {fail_count}")