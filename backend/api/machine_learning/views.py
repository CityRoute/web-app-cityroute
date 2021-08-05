from rest_framework.response import Response
from rest_framework.decorators import api_view
from backend.api.models import Route, Stop, RouteStop
from backend.api.serializer import StopSerializer
from rest_framework import status

@api_view(['GET'])
def StopToStopModelView(request):
    """
    Retrieve the stop to stop model result
    """
    try:
        print(request.query_params)
        start_stop = request.query_params.get('start_stop').lower()
        end_stop = request.query_params.get('end_stop').lower()
        route_num = request.query_params.get('route_num')
        num_stops = request.query_params.get('num_stops')
        # start_stop = Stop.objects.filter(name="College Street")
        # end_stop = Stop.objects.get(number=1934)
        # start_stop = "College Street"
        # end_stop = "Dame Street, stop 1934"
        all_stops = GetAllStops(start_stop, end_stop, route_num, num_stops)
        print(all_stops)
    except Exception as e:
        print(e)
        return Response({"error": "Error in getting journey time"}, status=status.HTTP_404_NOT_FOUND)
    return Response({"duration": 10})

# def GetStopPrediction(stop_id, route):

def GetStopModel(stop, route_model, outbound_yn):
    """
    Get the stop model
    """
    if stop.find('stop') != -1:
        print("stop in string", stop)
        stop_split = stop.split(' ')
        stop_number = stop_split[-1]
        if outbound_yn == None:
            stop_model = Stop.objects.get(
                routestops__routeid=route_model,
                number=stop_number
            )
        else:
            stop_model = Stop.objects.get(
                routestops__routeid=route_model,
                routestops__outbound_yn=outbound_yn,
                number=stop_number
            )
    else:
        print("stop in name", stop)
        if outbound_yn == None:
            stop_model = Stop.objects.get(
                routestops__routeid=route_model,
                name=stop
            )
        else:
            stop_model = Stop.objects.get(
                routestops__routeid=route_model,
                routestops__outbound_yn=outbound_yn,
                name=stop
            )
    print(stop_model)
    return stop_model

def GetAllStops(start_stop, end_stop, route, num_stops):
    """
    Get the stops between the start and end stops
    """
    # get the route model for the route
    route_model = Route.objects.get(routeid=route.upper())

    if start_stop.find('stop') != -1:
        start_stop_model = GetStopModel(start_stop, route_model, None)
    elif end_stop.find('stop') != -1:
        start_stop_model = GetStopModel(end_stop, route_model, None)
    else:
        try:
            start_stop_model = GetStopModel(start_stop, route_model, None)
        except:
            start_stop_model = GetStopModel(end_stop, route_model, None)

    # try outbound first
    outbound_yn =  start_stop_model.routestops.values('outbound_yn')[0]['outbound_yn']
    relevant_stops = RouteStop.objects.filter(routeid=route_model, outbound_yn=outbound_yn)
    relevant_start_stop = relevant_stops.get(stopnumber=start_stop_model)

    print(relevant_start_stop.order, num_stops)
    num_stops = int(num_stops)
    if outbound_yn:
        print("outbound")
        relevant_stops = RouteStop.objects.filter(routeid=route_model, outbound_yn=True, order__range=(relevant_start_stop.order, relevant_start_stop.order+num_stops))
    else:
        print("inbound")
        relevant_stops = RouteStop.objects.filter(routeid=route_model, outbound_yn=False, order__range=(relevant_start_stop.order-num_stops, relevant_start_stop.order))
    
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
