from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from .models import Message, MessageSerializer, Weather, User, Stop, FavouriteStop, Review
import pandas as pd
from django.http import JsonResponse
from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from .serializer import RegisterSerializer, UserSerializer, WeatherSerializer, StopSerializer, FavouriteStopSerializer
from django.contrib.auth.models import User
from .serializer import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated   
from django.db import IntegrityError
# from django.db import AssertionError
from django.http import HttpResponse





# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

#Register API
class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user,    context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })

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
    weather = Weather.objects.filter(day_number=day_number)
    serializer = WeatherSerializer(weather, many=True)
    print(serializer.data)
    return Response(serializer.data)

@api_view(['GET'])
def getAllStops(request):
    stops = Stop.objects.all()
    serializer = StopSerializer(stops, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def FavouriteStopsAll(request):
    """
    Retrieve all users' favourite bus stops
    """
    user = FavouriteStop.objects.all()
    serializer = FavouriteStopSerializer(user, many=True)
    print(serializer.data)
    return Response(serializer.data)


@api_view(['GET'])
def FavouriteStops(request):
    """
    Retrieve currently logged in user's favourited bus stops. 
    To test, get the accessToken from dev tools and use Postman: key= 'Authorization', value= 'Bearer {accessToken}'
    """
    userid = request.user.id
    user = User.objects.get(id=userid)
    stops = user.favstops.all()
    data = []
    for s in stops:
        data.append({
            'name': s.stopid.name, 
            'number' : s.stopid.number,
            'unique_id' : s.stopid.unique_id,
            'latitude': s.stopid.latitude,
            'longitude': s.stopid.longitude

        })

    return Response(data)

@api_view(['POST', 'GET'])
def addFavStop(request, number):
    """ 
    Add favourite stop of currently logged in user by number. 
    Currently works with the URL: http://localhost:8000/api/add-fav-stop/<number> 
    """
    
    try:
        user = request.user
        if Stop.objects.filter(number=number).exists():
            stop = Stop.objects.get(number=number)
            s = FavouriteStop(user=user, stopid=stop)
            s.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            print("Stop does not exist.")
    except IntegrityError as e:
        return HttpResponse("Error: Stop is already a favourite for this user.")
    except AssertionError as e:
        return HttpResponse("Error: Stop number does not exist.")





@api_view(['POST', 'GET'])
def writeReview(request, title, content):
    """
    Write review from logged in user's account & save to Review model/table in db
    """
    
    user = request.user
    r = Review(user=user, title=title, content=content)
    r.save()
    return Response(status=status.HTTP_201_CREATED)

    


