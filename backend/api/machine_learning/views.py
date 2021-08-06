from rest_framework.response import Response
from rest_framework.decorators import api_view
from backend.api.models import Route, Stop, RouteStop, Weather
from backend.api.serializer import StopSerializer
from rest_framework import status
from django.forms.models import model_to_dict

import datetime
import holidays
import numpy
import calendar


@api_view(['GET'])
def RouteModelView(request):
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
        # all_stops = GetAllStops(start_stop, end_stop, route_num, num_stops)
        all_features = GetAllRouteModelFeatures()
        # print("all_stops", all_stops)
        print("all_features", all_features, " length of array:", len(all_features))
    except Exception as e:
        print(e)
        return Response({"error": "Error in getting journey time"},
                        status=status.HTTP_404_NOT_FOUND)
    return Response({"duration": 10})


def GetAllRouteModelFeatures():
    required_features = [
        'HOUR',
        'DAYOFWEEK_Tuesday',
        'DAYOFWEEK_Wednesday',
        'DAYOFWEEK_Thursday',
        'DAYOFWEEK_Friday',
        'DAYOFWEEK_Saturday',
        'DAYOFWEEK_Sunday',
        'MONTHOFSERVICE_February',
        'MONTHOFSERVICE_March',
        'MONTHOFSERVICE_April',
        'MONTHOFSERVICE_May',
        'MONTHOFSERVICE_June',
        'MONTHOFSERVICE_July',
        'MONTHOFSERVICE_August',
        'MONTHOFSERVICE_September',
        'MONTHOFSERVICE_October',
        'MONTHOFSERVICE_November',
        'MONTHOFSERVICE_December',
        'IS_HOLIDAY_1',
        'humidity',
        'rain_1h',
        'temp',
        'wind_speed',
        'weather_main_Clouds',
        'weather_main_Drizzle',
        'weather_main_Fog',
        'weather_main_Mist',
        'weather_main_Rain',
        'weather_main_Smoke',
        'weather_main_Snow',
    ]
    dt = datetime.datetime.today()
    datetime_features_dict = GetDatetimeFeaturesRoute(dt)
    weather_features_dict = GetWeather(dt)
    all_features_dict = {**datetime_features_dict, **weather_features_dict}
    filtered_all_features_dict = {k: v for k, v in all_features_dict.items() if k in required_features}
    reordered_all_features_dict = {k: filtered_all_features_dict[k] for k in required_features}
    print(reordered_all_features_dict)

    numpy_features_array = numpy.array(list(reordered_all_features_dict.values()))
    return numpy_features_array


@api_view(['GET'])
def StopToStopModelView(request):
    """
    Retrieve the stop to stop model result
    """
    try:
        # print(request.query_params)
        start_stop = request.query_params.get('start_stop').lower()
        end_stop = request.query_params.get('end_stop').lower()
        route_num = request.query_params.get('route_num')
        num_stops = request.query_params.get('num_stops')
        # start_stop = Stop.objects.filter(name="College Street")
        # end_stop = Stop.objects.get(number=1934)
        # start_stop = "College Street"
        # end_stop = "Dame Street, stop 1934"
        all_stops = GetAllStops(start_stop, end_stop, route_num, num_stops)
        # print(all_stops)
    except Exception as e:
        # print(e)
        return Response({"error": "Error in getting journey time"},
                        status=status.HTTP_404_NOT_FOUND)
    return Response({"duration": 10})


# def GetStopPrediction(stop_id, route):


def GetStopModel(stop, route_model, outbound_yn):
    """
    Get the stop model
    """
    if stop.find('stop') != -1:
        # print("stop in string", stop)
        stop_split = stop.split(' ')
        stop_number = stop_split[-1]
        if outbound_yn == None:
            stop_model = Stop.objects.get(routestops__routeid=route_model,
                                          number=stop_number)
        else:
            stop_model = Stop.objects.get(routestops__routeid=route_model,
                                          routestops__outbound_yn=outbound_yn,
                                          number=stop_number)
    else:
        # print("stop in name", stop)
        if outbound_yn == None:
            stop_model = Stop.objects.get(routestops__routeid=route_model,
                                          name=stop)
        else:
            stop_model = Stop.objects.get(routestops__routeid=route_model,
                                          routestops__outbound_yn=outbound_yn,
                                          name=stop)
    # print(stop_model)
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
    outbound_yn = start_stop_model.routestops.values(
        'outbound_yn')[0]['outbound_yn']
    relevant_stops = RouteStop.objects.filter(routeid=route_model,
                                              outbound_yn=outbound_yn)
    relevant_start_stop = relevant_stops.get(stopnumber=start_stop_model)

    # print(relevant_start_stop.order, num_stops)
    num_stops = int(num_stops)
    if outbound_yn:
        # print("outbound")
        relevant_stops = RouteStop.objects.filter(
            routeid=route_model,
            outbound_yn=True,
            order__range=(relevant_start_stop.order,
                          relevant_start_stop.order + num_stops))
    else:
        # print("inbound")
        relevant_stops = RouteStop.objects.filter(
            routeid=route_model,
            outbound_yn=False,
            order__range=(relevant_start_stop.order - num_stops,
                          relevant_start_stop.order))

    # get the stops as a list of dictionaries
    relevant_stops = relevant_stops.values("stopnumber_id")

    # convert list of dictionaries to list of ids
    relevant_stops = [d['stopnumber_id'] for d in relevant_stops]

    return relevant_stops


# @api_view(['GET'])
# def GetLists(self):
#     dt = datetime.datetime.today()
#     weatherlist = GetWeather(dt)
#     rainlist = weatherlist[0]
#     weatherlist = weatherlist[1]
#     dtlist = GetDatetimeFeatures(dt)
#     combined_lists = [*rainlist, *dtlist, *weatherlist]
#     output = numpy.array(combined_lists)
#     return Response(output)


def GetWeather(dt):
    """
    Return a list for the binary weather features
    """
    today = datetime.datetime.today().date()
    dt = dt.date()  # assuming dt will be a datetime object
    try:
        # find the latest instance of the relevant date in the Weather model
        weather_obj = Weather.objects.get(scraped_on__date=today,
                                          datetime__date=dt)

        weather_features_list = [
            'humidity', 'rain_1h', 'temp', 'wind_speed', 'weather_main_Clear',
            'weather_main_Clouds', 'weather_main_Drizzle', 'weather_main_Fog',
            'weather_main_Mist', 'weather_main_Rain', 'weather_main_Smoke',
            'weather_main_Snow'
        ]
        weather_features_dict = {el: 0 for el in weather_features_list}
        # print(weather_features_dict)
        weather_obj_values = model_to_dict(weather_obj)
        # print(weather_obj_values)

        weather_features_dict['humidity'] = weather_obj_values['humidity']
        weather_features_dict['rain_1h'] = weather_obj_values['rain'] / 24
        weather_features_dict['temp'] = weather_obj_values['temp_day']
        weather_features_dict['wind_speed'] = weather_obj_values['windSpeed']

        weather_main_features = [
            'Clear', 'Clouds', 'Drizzle', 'Fog', 'Mist', 'Rain', 'Smoke',
            'Snow'
        ]
        for feature in weather_main_features:
            weather_features_dict["weather_main_" + feature] = int(
                weather_obj_values['main'] == feature)
            return weather_features_dict
        else:
            return "Cannot make prediction as weather code is unknown to the model."
    except Weather.DoesNotExist:
        return "No weather data available for this day."


def GetDatetimeFeaturesRoute(dt):
    """
    Returns a list (len 23), containing all the binary datetime features to be fed into the model
    """
    # get day of the week (0-6) and month (1-12)

    datetime_features_list = [
        'HOUR',
        'DAYOFWEEK_Monday',
        'DAYOFWEEK_Tuesday',
        'DAYOFWEEK_Wednesday',
        'DAYOFWEEK_Thursday',
        'DAYOFWEEK_Friday',
        'DAYOFWEEK_Saturday',
        'DAYOFWEEK_Sunday',
        'MONTHOFSERVICE_January',
        'MONTHOFSERVICE_February',
        'MONTHOFSERVICE_March',
        'MONTHOFSERVICE_April',
        'MONTHOFSERVICE_May',
        'MONTHOFSERVICE_June',
        'MONTHOFSERVICE_July',
        'MONTHOFSERVICE_August',
        'MONTHOFSERVICE_September',
        'MONTHOFSERVICE_October',
        'MONTHOFSERVICE_November',
        'MONTHOFSERVICE_December',
        'IS_HOLIDAY_1',
        'IS_WEEKDAY_1',
    ]
    datetime_features_dict = {el: 0 for el in datetime_features_list}
    date = dt.date()
    datetime_features_dict["HOUR"] = datetime.datetime.now().hour

    for day in filter(lambda k: 'DAYOFWEEK_' in k, datetime_features_list):
        print(day)
        if calendar.day_name[date.weekday()] in day:
            datetime_features_dict[day] = 1

    for month in filter(lambda k: 'MONTHOFSERVICE_' in k,
                        datetime_features_list):
        print(month)
        if calendar.month_name[date.month] in month:
            datetime_features_dict[month] = 1

    # get holiday yes/no, need to pipenv install holidays
    irish_holidays_2021 = []
    for date in holidays.Ireland(years=2021).items():
        irish_holidays_2021.append(str(date[0]))

    datetime_features_dict["IS_HOLIDAY_1"] = (1 if str(date).split()[0]
                                              in irish_holidays_2021 else 0)

    # get weekday yes/no
    datetime_features_dict["IS_WEEKDAY_1"] = (1
                                              if int(dt.weekday()) < 5 else 0)

    # print(datetime_features_dict)

    return datetime_features_dict


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
    output = [*dayofweeklist, *monthlist, *isholidaylist, *isweekdaylist]
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
