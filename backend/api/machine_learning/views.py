from rest_framework.response import Response
from rest_framework.decorators import api_view
from backend.api.models import Route, Stop, RouteStop

@api_view(['GET'])
def StopToStopModelView(request):
    """
    Retrieve the stop to stop model result
    """
    print(request.query_params)
    start_stop = request.query_params.get('start_stop')
    end_stop = request.query_params.get('end_stop')
    route_num = request.query_params.get('route_num')
    data = ""
    # start_stop = Stop.objects.filter(name="College Street")
    end_stop = Stop.objects.get(number=1934)
    print(start_stop, end_stop)
    return Response(start_stop)

# def GetStopPrediction(stop_id, route):

def GetAllStops(start_stop, end_stop, route):
    """
    Get the stops between the start and end stops
    """
    stops_lists = []
    return stops_lists

# def GetNearestStopByRoute(start_stop, end_stop, route):
#     relevant_stops = RouteStop.objects.filter(routeid=route)
#     stops = []
#     for i, stop in enumerate(relevant_stops):
#         stops.append({'num': stop.stopnumber.number, 'lat': stop.stopnumber.latitude, 'lon': stop.stopnumber.longitude})
#     closest_start = closest(stops, start_stop)['num']
#     closest_end = closest(stops, end_stop)['num']
#     print(closest(stops, end_stop))
#     for i, stop in enumerate(stops):
#         if stop['num'] == closest_start:
#             start_stop = i
#         if stop['num'] == closest_end:
#             end_stop = i
#     print(start_stop, end_stop)
#     return stops[start_stop:end_stop]

#     """
#     Get the prediction for the stop
#     """
#     return []


# from math import cos, asin, sqrt

# def distance(lat1, lon1, lat2, lon2):
#     p = 0.017453292519943295
#     hav = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
#     return 12742 * asin(sqrt(hav))

# def closest(data, v):
#     return min(data, key=lambda p: distance(v['lat'],v['lon'],p['lat'],p['lon']))
