from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from .models import Message, MessageSerializer, Weather, User, Stop, FavouriteStop
import pandas as pd
from django.http import JsonResponse
from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from .serializer import RegisterSerializer, UserSerializer, WeatherSerializer, FavouriteStopSerializer
from django.contrib.auth.models import User
from .serializer import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated   
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required



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
def FavouriteStopsAll(request):
    """
    Retrieve all users' favourite bus stops
    """
    user = FavouriteStop.objects.all()
    serializer = FavouriteStopSerializer(user, many=True)
    print(serializer.data)
    return Response(serializer.data)

# @api_view(['GET'])
# def FavouriteStops(request, username):
#     """
#     Retrieve a given user's favourited bus stops
#     """
#     user = User.objects.get(username=username)
#     stops = user.favstops.all()

#     serializer = FavouriteStopSerializer(stops, many=True)
#     print(serializer.data)
#     return Response(serializer.data)


# @login_required(login_url='/accounts/login/')
@api_view(['GET'])
def FavouriteStops(request):
    """
    Retrieve a given user's favourited bus stops
    """
    print(request.user.is_anonymous)
    # username = request.POST.get('tester', False)
    # password = request.POST.get('password')
    # user = authenticate(request, username=username, password=password)
    # if user is not None:
    #     login(request, user)
    #     print('login successful')
    # else:
    #     print('invalid login error')


    user = request.user.id
    print(user)
    objs = User.objects.get(id=user)
    # user = request.user
    stops = objs.favstops.all()
    serializer = FavouriteStopSerializer(stops, many=True)
    print(serializer.data)
    return Response(serializer.data)


    # if request.user.is_authenticated:
    #     stops = user.favstops.all()

    #     serializer = FavouriteStopSerializer(stops, many=True)
    #     print(serializer.data)
    #     return Response(serializer.data)
    # else:
    #     print("User not authenticated")
    #     return

    


