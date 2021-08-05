from rest_framework.response import Response
from rest_framework.decorators import api_view
from backend.api.models import Route, Stop, RouteStop, Weather
from backend.api.serializer import StopSerializer

import datetime
import holidays
import numpy

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

@api_view(['GET'])
def GetLists(self):
    dt = datetime.datetime.today()
    weatherlist = GetWeather(dt)
    rainlist = weatherlist[0]
    weatherlist = weatherlist[1]
    dtlist = GetDatetimeFeatures(dt)
    combined_lists = [*rainlist, *dtlist, *weatherlist]
    output = numpy.array(combined_lists)
    return Response(output)

    

def GetWeather(dt):
    """
    Return a list for the binary weather features
    """
    today = datetime.datetime.today().date()
    dt = dt.date() # assuming dt will be a datetime object
    try:
        # find the latest instance of the relevant date in the Weather model
        obj = Weather.objects.get(scraped_on__date=today, datetime__date=dt)

        # make a list of 0s and 1 to feed to the pickle model
        rain = [obj.rain]
        weatherlist = [0] * 7
        dict = {
            "Clear":0,
            "Clouds":1,
            "Drizzle":2,
            "Fog":3,
            "Mist":4,
            "Rain":5,
            "Snow":6
        }
        if obj.main in dict:
            weatherlist[dict[obj.main]] = 1
            return [rain, weatherlist]
        else:
            return "Cannot make prediction as weather code is unknown to the model."
    except Weather.DoesNotExist:
        return "No weather data available for this day."
    
        

def GetDatetimeFeatures(dt):
    """
    Returns a list (len 23), containing all the binary datetime features to be fed into the model
    """       
    # get day of the week (0-6) and month (1-12)
    date = dt.date()
    print("Date: {}".format(date))
    dayofweek = date.weekday()
    month = dt.month
    print("Month: {}, weekday: {}".format(month, dayofweek))
    
    # get holiday yes/no, need to pipenv install holidays
    irish_holidays_2021 = []
    for date in holidays.Ireland(years=2021).items():
        irish_holidays_2021.append(str(date[0]))
        
    is_holiday = (1 if str(date).split()[0] in irish_holidays_2021 else 0)
    print("Holiday?: {}".format(is_holiday))
    
    # get weekday yes/no
    is_weekday = (1 if int(dt.weekday()) < 5 else 0)
    print("Weekday?: {}".format(is_weekday))
    
    # 0s and 1 in weekday list
    dayofweeklist = [0] * 7
    order = [4, 0, 5, 6, 3, 1, 2]
    dayofweeklist[order.index(dayofweek)] = 1
    print("Dayofweek list: {}".format(dayofweeklist))
    
    # 0s and 1 for month list
    monthlist = [0] * 12
    order = [4, 8, 12, 2, 1, 7, 6, 3, 5, 11, 10, 9]
    monthlist[order.index(month)] = 1
    print("Month list: {}".format(monthlist))
    
    # 0 and 1 for is_holiday list
    # if it is a holiday, column 0 is 0 and column 1 is 1, and vice versa
    isholidaylist = [0] * 2
    if is_holiday == 1:
        isholidaylist[1] = 1
    else:
        isholidaylist[0] = 1
    print("isholiday list: {}".format(isholidaylist))
    
    # 0 and 1 for is_weekday list
    # if it is a weekday, column 0 is 0 and column 1 is 1, and vice versa
    isweekdaylist = [0] * 2
    if is_weekday == 1:
        isweekdaylist[1] = 1
    else:
        isweekdaylist[0] = 1
    print("isweekday list: {}".format(isweekdaylist))
    
    # combine all the lists in the right order for model input
    output = [*dayofweeklist,*monthlist,*isholidaylist,*isweekdaylist]
    return output

    



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
