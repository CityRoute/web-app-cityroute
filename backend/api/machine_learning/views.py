from rest_framework.response import Response
from rest_framework.decorators import api_view
from backend.api.models import Route, Stop, RouteStop
from backend.api.serializer import StopSerializer

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
    # end_stop = Stop.objects.get(number=1934)
    start_stop = "College Street"
    end_stop = "Dame Street, stop 1934"
    return Response(GetAllStops(start_stop, end_stop, "54a", 2))

# def GetStopPrediction(stop_id, route):

def GetStopModel(stop):
    """
    Get the stop model
    """
    if stop.find('stop') != -1:
        stop_split = stop.split(' ')
        stop_number = stop_split[-1]
        stop_model = Stop.objects.get(number=stop_number)
    else:
        stop_model = Stop.objects.get(name=stop)
    return stop_model

def GetAllStops(start_stop, end_stop, route, num_stops):
    """
    Get the stops between the start and end stops
    """

    # get the stop models for both of the stops
    start_stop_model = GetStopModel(start_stop)
    end_stop_model = GetStopModel(end_stop)

    # get the route model for the route
    route_model = Route.objects.get(routeid=route.upper())

    # try outbound first
    relevant_stops = RouteStop.objects.filter(routeid=route_model, outbound_yn=True)
    relevant_start_stop = relevant_stops.get(stopnumber=start_stop_model)
    relevant_end_stop = relevant_stops.get(stopnumber=end_stop_model)
    if relevant_start_stop.order + num_stops == relevant_end_stop.order:
        relevant_stops = RouteStop.objects.filter(routeid=route_model, outbound_yn=True, order__range=(relevant_start_stop.order, relevant_end_stop.order))
        print("outbound")
    else:
        # if outbound fails above use inbound
        relevant_stops = RouteStop.objects.filter(routeid=route_model, outbound_yn=False)
        relevant_start_stop = relevant_stops.get(stopnumber=start_stop_model)
        relevant_end_stop = relevant_stops.get(stopnumber=end_stop_model)
        relevant_stops = RouteStop.objects.filter(routeid=route_model, outbound_yn=False, order__range=(relevant_end_stop.order, relevant_start_stop.order))
        print("inbound")
    
    # get the stops as a list of dictionaries
    relevant_stops = relevant_stops.values("stopnumber_id")

    # convert list of dictionaries to list of ids
    relevant_stops = [d['stopnumber_id'] for d in relevant_stops]

    return relevant_stops

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
