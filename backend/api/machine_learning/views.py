from rest_framework.response import Response
from rest_framework.decorators import api_view

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
    return Response(start_stop)

def GetAllStops(start_stop, end_stop, route):
    """
    Get the stops between the start and end stops
    """
    stops_lists = []
    return stops_lists

def GetStopPrediction(stop_id, route):
    """
    Get the prediction for the stop
    """
    return []