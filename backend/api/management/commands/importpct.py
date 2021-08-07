from django.core.management.base import BaseCommand

from backend.api.models import Route, RouteStop, Stop
import json

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        
        with open('backend/api/management/commands/stop_time_pct.json') as f:
            routes = json.load(f)

        total_count = 0
        fail_count = 0 
        for route_num, stop_list in routes.items():
            print(route_num)
            for stop_direction, stop_num_list in stop_list.items():
                outbound_yn = True if stop_direction == 'outbound' else False
                
                for stop_num, pct in stop_num_list.items():
                    total_count += 1
                    try:
                        rs = RouteStop.objects.get(routeid=route_num, stopnumber=stop_num, outbound_yn=outbound_yn)
                        rs.percent_of_route = pct
                        rs.save()
                        print("Stop number {}, percent: {}%".format(stop_num, pct))
                    except Exception as e:
                        print(e)
                        fail_count += 1
                        pass
        print(f"total: {total_count}, fail: {fail_count}")                   