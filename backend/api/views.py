from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from .models import Message, MessageSerializer, Weather
import pandas as pd
from django.http import JsonResponse
from .serializers import WeatherSerializer

# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


@api_view(['GET'])
def BusStopTimes(request, bus_stop):
    """
    Retrieve, update or delete a code snippet.
    """

    if request.method == 'GET':
        url = "https://www.dublinbus.ie/en/RTPI/Sources-of-Real-Time-Information/?searchtype=view&searchquery="
        df = pd.read_html(url+str(bus_stop))
        schedule = df[3]
        schedule = schedule.iloc[:, :-1]
        schedule.rename(
            columns={'Expected Time': 'Expected_Time'}, inplace=True)

        schedule = schedule.to_json(orient='records')

        print(schedule)
        return Response(json.loads(schedule))


@api_view(['GET'])
def WeatherByDay(request, day_number):
    """
    Retrieve the weather in Dublin on a given day within the next 16 days 
    (ie. From today = DAY 1, to (today+15 days) = DAY 16)
    """
    weather = Weather.objects.get(day_number=day_number)
    serializer = WeatherSerializer(weather, many=False)
    print(serializer.data)
    return Response(serializer.data)