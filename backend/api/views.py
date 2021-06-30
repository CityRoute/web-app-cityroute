from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from .models import Message, MessageSerializer
import pandas as pd
from django.http import JsonResponse
from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from .serializer import RegisterSerializer, UserSerializer
from django.contrib.auth.models import User

# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))


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
