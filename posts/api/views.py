from django.db.models import Q
from rest_framework.generics import (
        CreateAPIView,
        DestroyAPIView,
        ListAPIView,
        UpdateAPIView,
        RetrieveAPIView,
        RetrieveUpdateAPIView,
)
from ..models import Incident
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)

from twilio.rest import Client

# put your own credentials here

from rest_framework.filters import (
        SearchFilter,
        OrderingFilter,
)

from .permissions import IsOwnerOrReadOnly

from ..models import Incident
from .serializers import IncidentListSerializer, IncidentDetailSerializer, IncidentCreateUpdateSerializer
from rest_framework import status
from rest_framework.response import Response


from rest_framework import mixins
from rest_framework import generics
from django.http import HttpResponseRedirect
from django_filters.rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
#Start View
###
account_sid = "AC4b6a8c4025120465af4a05a6c948017f"
auth_token = "11557bb09bebac4ee0021cd2bc47b9c3"
###
client = Client(account_sid, auth_token)

class IncidentCreateAPIView(CreateAPIView) :
    queryset = Incident.objects.all()
    serializer_class = IncidentCreateUpdateSerializer
    #permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class IncidentCreateAPIViewNoUser(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView,) : #include all functions (Update, create function in one class)
    serializer_class = IncidentCreateUpdateSerializer
    def get(self, request): #Get Paramter from URL.
        deviceid = self.request.query_params.get('deviceid', None)
        crime = self.request.query_params.get('crime', None)
        crimedesc = self.request.query_params.get('crimedesc', None)
        latitude = self.request.query_params.get('lat', None)
        longitude = self.request.query_params.get('lng', None)
        incident = Incident.objects.create(deviceid = deviceid, crime=crime, crimedesc=crimedesc, latitude=latitude, longitude=longitude) #Create url format for adding incidents
        incident.save()
        return Response('okay')



class IncidentDetailAPIView(RetrieveAPIView) :
    queryset = Incident.objects.all()
    serializer_class = IncidentDetailSerializer
    lookup_field = 'id'


class IncidentUpdate(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView,): #include all functions (Update, create function in one class)
    serializer_class = IncidentCreateUpdateSerializer
    def get(self, request): #Get Paramter from url.
        deviceid = self.request.query_params.get('deviceid', None)
        crime = self.request.query_params.get('crime', None)
        crimedesc = self.request.query_params.get('crimedesc', None)
        lat = self.request.query_params.get('lat', None)
        lng = self.request.query_params.get('lng', None)
        Incident.objects.filter(deviceid = deviceid).update(crime=crime, crimedesc=crimedesc, latitude=lat, longitude=lng) #Create url format for updating incidents
        return Response('okay')


class IncidentDeleteAPIView(DestroyAPIView) :
    serializer_class = IncidentDetailSerializer
    def get(self, request):  #Get Paramter from url.
        deviceid = self.request.query_params.get('deviceid', None)
        Incident.objects.filter(deviceid=deviceid).delete() #Create URL to delete incidents
        return Response('okay')



class IncidentListAPIView(ListAPIView):
    serializer_class = IncidentListSerializer
    def get_queryset(self):
        pass
    def list(self,request, *args, **kwargs):
        crime = self.request.query_params.get('crime', None)
        deviceid = self.request.query_params.get('deviceid', None)
        crimes = []
        if crime is not None:
            splitcrime = crime.split(',')
            for word in splitcrime:
                crimes.append(word)
            queryset = Incident.objects.filter(crime__in = crimes).order_by('pk') #Filter by crime
            serializer_class = IncidentListSerializer(queryset, many=True)
            serialized_data =  ({'results': serializer_class.data,'status' : status.HTTP_200_OK, 'Message' : 'Filtered by crime = ' + ', '.join(crimes)}) #setting structure for API

        elif crime is None and deviceid is not None:
            queryset = Incident.objects.filter(deviceid__contains = deviceid).order_by('pk') #Filter by deviceid
            serializer_class = IncidentListSerializer(queryset, many=True)
            serialized_data =  ({'results': serializer_class.data,'status' : status.HTTP_200_OK, 'Message' : 'Filtered by id = ' + deviceid })  #setting structure for API
        else:
            queryset = Incident.objects.all().order_by('pk') #Filter by incident
            serializer_class = IncidentListSerializer(queryset, many=True)
            serialized_data =  ({'results': serializer_class.data,'status' : status.HTTP_200_OK, 'Message' : 'Allcrime'})  #setting structure for API

        return  Response(serialized_data)

