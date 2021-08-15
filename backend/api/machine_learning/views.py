from rest_framework.response import Response
from rest_framework.decorators import api_view
from backend.api.models import Route, Stop, RouteStop, Weather
from backend.api.serializer import StopSerializer
from rest_framework import status
from django.forms.models import model_to_dict
import pickle
from django.core.management.base import BaseCommand

import datetime
import holidays
import numpy
import calendar

route_model_required_features = [
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

stop_model_required_features = [
    'rain_1h', 'DAYOFWEEK_Friday', 'DAYOFWEEK_Monday', 'DAYOFWEEK_Saturday',
    'DAYOFWEEK_Sunday', 'DAYOFWEEK_Thursday', 'DAYOFWEEK_Tuesday',
    'DAYOFWEEK_Wednesday', 'MONTHOFSERVICE_April', 'MONTHOFSERVICE_August',
    'MONTHOFSERVICE_December', 'MONTHOFSERVICE_February',
    'MONTHOFSERVICE_January', 'MONTHOFSERVICE_July', 'MONTHOFSERVICE_June',
    'MONTHOFSERVICE_March', 'MONTHOFSERVICE_May', 'MONTHOFSERVICE_November',
    'MONTHOFSERVICE_October', 'MONTHOFSERVICE_September', 'IS_HOLIDAY_0',
    'IS_HOLIDAY_1', 'IS_WEEKDAY_0', 'IS_WEEKDAY_1', 'weather_main_Clear',
    'weather_main_Clouds', 'weather_main_Drizzle', 'weather_main_Fog',
    'weather_main_Mist', 'weather_main_Rain', 'weather_main_Snow'
]

stop_pair_model_required_features = [
    'DWELLTIME',
    'rain_1h',
    'MONTHOFSERVICE_April',
    'MONTHOFSERVICE_August',
    'MONTHOFSERVICE_December',
    'MONTHOFSERVICE_February',
    'MONTHOFSERVICE_January',
    'MONTHOFSERVICE_July',
    'MONTHOFSERVICE_June',
    'MONTHOFSERVICE_March',
    'MONTHOFSERVICE_May',
    'MONTHOFSERVICE_November',
    'MONTHOFSERVICE_October',
    'MONTHOFSERVICE_September',
    'DAYOFWEEK_Friday',
    'DAYOFWEEK_Monday',
    'DAYOFWEEK_Saturday',
    'DAYOFWEEK_Sunday',
    'DAYOFWEEK_Thursday',
    'DAYOFWEEK_Tuesday',
    'DAYOFWEEK_Wednesday',
    'IS_HOLIDAY_0',
    'IS_HOLIDAY_1',
    'IS_WEEKDAY_0',
    'IS_WEEKDAY_1',
    'eve_rushour_0',
    'eve_rushour_1',
    'morn_rushour_0',
    'morn_rushour_1',
    'weather_main_Clear',
    'weather_main_Clouds',
    'weather_main_Drizzle',
    'weather_main_Fog',
    'weather_main_Mist',
    'weather_main_Rain',
    'weather_main_Snow'
]


@api_view(['GET'])
def ModelPredictionView(request):
    """
    Retrieve the stop to stop model result
    """
    try:
        # print(request.query_params)
        start_stop = request.query_params.get('start_stop').lower()
        end_stop = request.query_params.get('end_stop').lower()
        route_num = request.query_params.get('route_num')
        num_stops = request.query_params.get('num_stops')

        all_stops = GetAllStops(start_stop, end_stop, route_num, num_stops)

        print("all_stops", all_stops)
        model_type = request.query_params.get('model_type').lower()
        print(model_type)
        
        if model_type == 'route':
            all_features = GetAllRequiredFeatures(
                route_model_required_features)
            print("all_features", all_features, " length of array:",
                  len(all_features))
            prediction = RoutePrediction(all_stops, all_features, route_num)

        else:
            all_features = GetAllRequiredFeatures(stop_model_required_features)
            print("all_features", all_features, " length of array:",
                  len(all_features))
            prediction = StopPrediction(all_stops, all_features)
        return Response({"prediction": prediction}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        # Try to predict with Stop Pair model instead
        try:
            # print(request.query_params)
            start_stop = request.query_params.get('start_stop').lower()
            end_stop = request.query_params.get('end_stop').lower()
            route_num = request.query_params.get('route_num')
            num_stops = request.query_params.get('num_stops')
            # all_stops = GetAllStops(start_stop, end_stop, route_num, num_stops)
            all_stops = [7363, 4588, 4589, 7364, 7365]
            print("all_stops", all_stops)

            model_type = request.query_params.get('model_type').lower()
            print(model_type)
            
            all_features = GetAllRequiredFeatures(stop_pair_model_required_features)
            pred = StopPairPrediction(all_stops, all_features)
            print('Stop Pair Model prediction:', pred)
            return Response({"prediction:": pred}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Error in getting journey time"},
                        status=status.HTTP_404_NOT_FOUND)

    

def RoutePrediction(all_stops, all_features, route):
    """
    Retrieve the route model prediction
    """
    # get first stop on route
    start_stop_model = Stop.objects.get(number=all_stops[0])

    # check if route is outbound or not from routestop
    outbound_yn = start_stop_model.routestops.values(
        'outbound_yn')[0]['outbound_yn']
    direction = 'outbound' if outbound_yn else 'inbound'

    # read in pickle file based on route and direction
    pkl_filename = f"backend/api/machine_learning/route_models/route_{route}_{direction}.pkl"
    with open(pkl_filename, 'rb') as file:
        pickle_model = pickle.load(file)

    # run prediction
    prediction = pickle_model.predict(numpy.array(all_features).reshape(1, -1))
    # print("Predicted time: ", prediction[0])

    # get the end stop
    end_stop_model = Stop.objects.get(number=all_stops[-1])

    # get percentage of route used up to first stop on journey
    start_stop_pct = start_stop_model.routestops.values(
        'percent_of_route')[0]['percent_of_route']

    # get percentage of route used up to last stop on journey
    end_stop_pct = end_stop_model.routestops.values(
        'percent_of_route')[0]['percent_of_route']

    # calculate the total dwell time based on dwell time for each stop on journey
    total_dwell_time = 0
    for stop in all_stops:
        stop_model = Stop.objects.get(number=stop)
        dwell_time = getattr(stop_model, 'avg_dwelltime')
        total_dwell_time += dwell_time

    # get the final prediction by only keeping the percentage of route used on the journey and adding the dwell time
    final_prediction = prediction * (
        (end_stop_pct - start_stop_pct) / 100) + total_dwell_time
    print(f"Predicted time: {final_prediction}")

    return final_prediction[0]


def StopPrediction(all_stops, all_features):
    """
    Retrieve the stop model prediction
    """
    prediction = 0
    for stop in all_stops:
        # read in pickle file based on stop
        pkl_filename = f"backend/api/machine_learning/stop_models/stop_{stop}.pkl"
        with open(pkl_filename, 'rb') as file:
            pickle_model = pickle.load(file)
        # run prediction
        prediction += pickle_model.predict(
            numpy.array(all_features).reshape(1, -1))

    return prediction[0]

def StopPairPrediction(all_stops, all_features):
    """
    Retrieve the stop pair model prediction
    """
    prediction = 0
    # List of stops that are the first stop for any route
    first_stops_list = []
    first_stop =  RouteStop.objects.filter(stopnumber=all_stops[0]).first() # many RouteStops with the same number, only need to look at 1 (eg. first)
    
    # check if route is outbound or not from routestop
    # outbound_yn = start_stop_model.routestops.values(
    #     'outbound_yn')[0]['outbound_yn']
    outbound_yn = getattr(first_stop, 'outbound_yn')
    direction = 'outbound' if outbound_yn == 1 else 'inbound'
    
    # Remove first element of all_stops if first_stop in all_stops
    if all_stops[0] == first_stop:
        all_stops = all_stops[1:]
        
        for previous, current in zip(all_stops, all_stops[1:]):
            filename = f"backend/api/machine_learning/stop_pair_models/stop_{current}_{previous}_{direction}.pkl"
            with open(filename, 'rb') as file:
                pickle_model = pickle.load(file)
            # Running prediction
            prediction += pickle_model.predict(numpy.array(all_features).reshape(1, -1))
    
    else:
        for previous, current in zip(all_stops, all_stops[1:]):
            filename = f"backend/api/machine_learning/stop_pair_models/stop_{current}_{previous}_{direction}.pkl"
            with open(filename, 'rb') as file:
                pickle_model = pickle.load(file)
            
            prediction += pickle_model.predict(numpy.array(all_features).reshape(1, -1))
    
    return prediction[0]

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

    start_stop_model = None
    end_stop_model = None
    if start_stop.find('stop') != -1 and end_stop.find('stop') != -1:
        start_stop_model = GetStopModel(start_stop, route_model, None)
        end_stop_model = GetStopModel(end_stop, route_model, None)
    elif start_stop.find('stop') != -1:
        start_stop_model = GetStopModel(start_stop, route_model, None)
    elif end_stop.find('stop') != -1:
        end_stop_model = GetStopModel(end_stop, route_model, None)
    else:
        try:
            start_stop_model = GetStopModel(start_stop, route_model, None)
        except:
            pass
        try:
            end_stop_model = GetStopModel(start_stop, route_model, None)
        except:
            pass

    # try outbound first
    if start_stop_model != None and end_stop_model != None:
        outbound_yn = start_stop_model.routestops.values(
            'outbound_yn')[0]['outbound_yn']
        relevant_stops = RouteStop.objects.filter(routeid=route_model,
                                                  outbound_yn=outbound_yn)
        relevant_start_stop = relevant_stops.get(stopnumber=start_stop_model)
        relevant_end_stop = relevant_stops.get(stopnumber=end_stop_model)
        relevant_stops = RouteStop.objects.filter(
            routeid=route_model,
            outbound_yn=True,
            order__range=(relevant_start_stop.order,
                            relevant_end_stop.order))
    elif start_stop_model != None:
        outbound_yn = start_stop_model.routestops.values(
            'outbound_yn')[0]['outbound_yn']
        relevant_stops = RouteStop.objects.filter(routeid=route_model,
                                                  outbound_yn=outbound_yn)
        relevant_start_stop = relevant_stops.get(stopnumber=start_stop_model)

        # print(relevant_start_stop.order, num_stops)
        num_stops = int(num_stops)
        relevant_stops = RouteStop.objects.filter(
            routeid=route_model,
            outbound_yn=True,
            order__range=(relevant_start_stop.order,
                            relevant_start_stop.order + num_stops))
    elif relevant_end_stop != None:
        outbound_yn = end_stop_model.routestops.values(
            'outbound_yn')[0]['outbound_yn']
        relevant_stops = RouteStop.objects.filter(routeid=route_model,
                                                  outbound_yn=outbound_yn)
        relevant_end_stop = relevant_stops.get(stopnumber=end_stop_model)

        # print(relevant_start_stop.order, num_stops)
        num_stops = int(num_stops)
        relevant_stops = RouteStop.objects.filter(
            routeid=route_model,
            outbound_yn=False,
            order__range=(relevant_end_stop.order - num_stops,
                            relevant_end_stop.order))
    else:
        return []
    # get the stops as a list of dictionaries
    relevant_stops = relevant_stops.values("stopnumber_id")

    # convert list of dictionaries to list of ids
    relevant_stops = [d['stopnumber_id'] for d in relevant_stops]
    print(relevant_stops)
    return relevant_stops


def GetAllRequiredFeatures(required_features=None):
    if required_features is None:
        return None
    # use current date for datetime features & weather features
    dt = datetime.datetime.today()

    # get datetime features
    datetime_features_dict = GetDatetimeFeatures(dt)
    print(datetime_features_dict)

    # get weather features
    weather_features_dict = GetWeatherFeatures(dt)
    print(weather_features_dict)

    # combine datetime and weather features into one dictionary
    all_features_dict = {**datetime_features_dict, **weather_features_dict}
    print(all_features_dict)

    # filter this dict with the required features
    filtered_all_features_dict = {
        k: v
        for k, v in all_features_dict.items() if k in required_features
    }

    # reorder the list to match the model spec
    reordered_all_features_dict = {
        k: filtered_all_features_dict[k]
        for k in required_features
    }

    # print("reordered_all_features_dict", reordered_all_features_dict)

    # convert to numpy array to match model spec
    numpy_features_array = numpy.array(
        list(reordered_all_features_dict.values()))
    return numpy_features_array


def GetWeatherFeatures(dt):
    """
    Return a list for the binary weather features
    """
    today = datetime.datetime.today().date()
    dt = dt.date()  # assuming dt will be a datetime object
    weather_features_list = [
        'humidity', 'rain_1h', 'temp', 'wind_speed', 'weather_main_Clear',
        'weather_main_Clouds', 'weather_main_Drizzle', 'weather_main_Fog',
        'weather_main_Mist', 'weather_main_Rain', 'weather_main_Smoke',
        'weather_main_Snow'
    ]

    try:
        # find the latest instance of the relevant date in the Weather model
        weather_obj = Weather.objects.get(scraped_on__date=today,
                                          datetime__date=dt)

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
            return {k: 0 for v, k in enumerate(weather_features_list)}
    except Weather.DoesNotExist:
        return {k: 0 for v, k in enumerate(weather_features_list)}


def GetDatetimeFeatures(dt, stop_number=7365): # stop arg only applies to stop-pair model
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
        'IS_HOLIDAY_0',
        'IS_WEEKDAY_1',
        'IS_WEEKDAY_0',
        'DWELLTIME',
        'eve_rushour_0',
        'eve_rushour_1',
        'morn_rushour_0',
        'morn_rushour_1'
    ]
    datetime_features_dict = {el: 0 for el in datetime_features_list}
    date = dt.date()
    datetime_features_dict["HOUR"] = datetime.datetime.now().hour

    for day in filter(lambda k: 'DAYOFWEEK_' in k, datetime_features_list):
        # print(day)
        if calendar.day_name[date.weekday()] in day:
            datetime_features_dict[day] = 1

    for month in filter(lambda k: 'MONTHOFSERVICE_' in k,
                        datetime_features_list):
        # print(month)
        if calendar.month_name[date.month] in month:
            datetime_features_dict[month] = 1

    # get holiday yes/no, need to pipenv install holidays
    # irish_holidays_2021 = []
    # print(holidays.Ireland(years=2021).keys())
    # for date in holidays.Ireland(years=2021).items():
    #     irish_holidays_2021.append(str(date[0]))
    datetime_features_dict["IS_HOLIDAY_1"] = (1 if date in holidays.Ireland(
        years=2021).keys() else 0)

    datetime_features_dict["IS_HOLIDAY_0"] = (0 if date in holidays.Ireland(
        years=2021).keys() else 1)
    # get weekday yes/no
    datetime_features_dict["IS_WEEKDAY_1"] = (1
                                              if int(dt.weekday()) < 5 else 0)

    datetime_features_dict["IS_WEEKDAY_0"] = (0
                                              if int(dt.weekday()) < 5 else 1)


    stop = Stop.objects.get(number=stop_number)
    datetime_features_dict["DWELLTIME"] = getattr(stop, 'avg_dwelltime')
    # print(getattr(stop, 'avg_dwelltime'))

    datetime_features_dict['eve_rushour'] = (1 if int(dt.hour) >= 16 and int(dt.hour) <= 19 else 0)
    datetime_features_dict['morn_rushour'] = (1 if int(dt.hour) >= 7 and int(dt.hour) <= 9 else 0)
    # print(datetime_features_dict)

    return datetime_features_dict