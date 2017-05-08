from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .models import Safeplace
from .serializers import SafeplaceCreateUpdateSerializer, SafeplaceDetailSerializer, SafeplaceListSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser,IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
import math
from itertools import chain
from django.http import HttpResponseRedirect

#### DEFINE MATH FUNCTION ####
def distance(lat1, long1, lat2, long2):
    R = 6371 # Earth Radius in Km
    dLat = math.radians(lat2 - lat1) # Convert Degrees 2 Radians
    dLong = math.radians(long2 - long1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLong/2) * math.sin(dLong/2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d
##############################




class SafeplaceCreateAPIView(CreateAPIView):
    queryset = Safeplace.objects.all()
    serializer_class = SafeplaceCreateUpdateSerializer
    permission_classes = [IsAuthenticated]


class SafeplaceListAPIView(ListAPIView):
    serializer_class = SafeplaceListSerializer
    def get_queryset(self):
        pass
    def list(self, request):
        queryset = Safeplace.objects.all()
        type = self.request.query_params.get('type', None) #get parameters from url
        postcode = self.request.query_params.get('postcode', None)  #get parameters from url
        suburb = self.request.query_params.get('suburb', None)#define the URL format
        try:
            postcode = postcode.split(',') #spilt two postcode by comma
        except (AttributeError, TypeError):
            pass
        try:
            type = type.split(',') #spilt two types by comma
        except (AttributeError, TypeError):
            pass
        try:
            suburb = suburb.split(',') #spit two sububrs by comma
        except (AttributeError, TypeError):
            pass
        try:
            if postcode is not None:
                queryset = queryset.filter(type__in=int(postcode))
            if type is not None:
                    queryset = queryset.filter(type__in=type) #filter by type
                    serializer_class = SafeplaceListSerializer(queryset, many=True)
                    serialized_data = ({'results': serializer_class.data, 'status': status.HTTP_200_OK, 'message': type}) #define your json message
                    return Response(serialized_data)
            elif type is not None and suburb is not None:
                queryset = queryset.filter(type__in=type, suburb__in=suburb) #filter by suburb
            elif type is None and suburb is not None:
                    queryset = queryset.filter(suburb__in=suburb)
            elif type is not None and suburb is None:
                    queryset = queryset.filter(type__in=type)
            elif type is None and suburb is None:
                    queryset = Safeplace.objects.all()
            serializer_class = SafeplaceListSerializer(queryset, many=True)
            serialized_data = ({'results': serializer_class.data, 'status': status.HTTP_200_OK, 'message': suburb}) #API stucture.
            return Response(serialized_data)
        except (AttributeError, TypeError):
            queryset = Safeplace.objects.all()
            serializer_class = SafeplaceListSerializer(queryset, many=True)
            serialized_data = ({'results': serializer_class.data, 'status': status.HTTP_404_NOT_FOUND, 'message': ''}) #API stucture.
        return Response(serialized_data)


class SafeplaceDetailAPIView(ListAPIView):
    serializer_class = SafeplaceDetailSerializer
    def get_queryset(self):
            pass
    def list(self, requests):
        queryset = Safeplace.objects.all()
        lat = float(self.request.query_params.get('lat', None)) #get lat from url
        lng = float(self.request.query_params.get('lng', None)) #get long from url

        if lat is not None and lng is not None: #check if there is lat and lng
            obj = [] #for 2km
            obj_5 = [] #for 5km
            dict_dis = {} #dictionary include distance for 2km
            dict_dis5 = {}  #dictionary include distance for 5km
            sort_object = [] #extract index from dictionary for 2km
            sort_object5 = [] #extract index from dictionary for 5km
            latList = [] #contain lat
            lngList = [] #contain lng

            data = Safeplace.objects.order_by('pk') #order the data by ID asc
            for x in data:
                latList.append(x.latitude) #append lat and lng to the list
                lngList.append(x.longitude)
            for x in range(0, len(data)):
                latx = float(latList[x]) #make lat into float
                lngx = float(lngList[x]) #make lng into float
                km = distance(lat, lng, latx, lngx) #include maths function
                #Change distances
                if km <= 1:           #compensating distance
                    obj.append(x+1)
                    dict_dis[x+1] = km
                elif km < 5:         #if the km is less than 5km, show everything
                    obj_5.append(x+1)
                    dict_dis5[x+1] = km
                # elif km > 1:
                #     obj_false.append(km) #if fail, append safeplaces outside 2km
                #     pk_false.append(x+1)
            if len(obj) != 0:
                msg = '2 KM' #show message if is 2km
                #sort = sorted(sorted(dict_dis.items()),reverse=True)
                sort = [(k, dict_dis[k]) for k in sorted(dict_dis, key=dict_dis.get, reverse=True)] #sort the distance from the highest to the lowest distance
                for x in range(0,len(sort)):
                    sortout = sort[x][x-x]   #extracting the dictionary
                    sort_object.append(sortout) #append
                clauses = ' '.join(['WHEN id=%s THEN %s' % (pk, i) for i, pk in enumerate(sort_object)])  #search for the id in order and lock the position
                ordering = 'CASE %s END' % clauses  #lock position for the function call extra
                queryset = Safeplace.objects.filter(pk__in=sort_object).extra(select={'ordering': ordering}, order_by=('ordering',)) #Searching queryset by the id listed. Apply the locking condition so that the id would not be arrange from highest to lowest
                serializer_class = SafeplaceDetailSerializer(queryset, many=True)
                serialized_data =  ({'results': serializer_class.data,'status' : status.HTTP_200_OK, 'message' : msg}) #setting the json format.
            elif len(obj) == 0 and len(obj_5) != 0: #if length is less than 5km
                msg = '5 KM'
                sort5 = [(k, dict_dis5[k]) for k in sorted(dict_dis5, key=dict_dis5.get, reverse=True)] #sort the distance from the highest to the lowest distance
                for x in range(0,len(sort5)):
                    sortout = sort5[x][x-x]  #extracting the dictionary
                    sort_object5.append(sortout)  #append
                clauses5 = ' '.join(['WHEN id=%s THEN %s' % (pk, i) for i, pk in enumerate(sort_object5)])  #search for the id in order and lock the position
                ordering5 = 'CASE %s END' % clauses5
                queryset = Safeplace.objects.filter(pk__in=sort_object5).extra(select={'ordering': ordering5}, order_by=('ordering',)) #Searching queryset by the id listed. Apply the locking condition so that the id would not be arrange
                serializer_class = SafeplaceDetailSerializer(queryset, many=True)
                serialized_data = ({'results': serializer_class.data, 'status': status.HTTP_200_OK, 'message': msg}) #setting the json format.
            elif len(obj) == 0 and len(obj_5) == 0:
                msg = 'Nothing found'  #if there is no result in the query
                queryset = Safeplace.objects.filter(pk__in=obj_5)
                serializer_class = SafeplaceDetailSerializer(queryset, many=True)
                serialized_data = (
                {'results': serializer_class.data, 'status': status.HTTP_404_NOT_FOUND, 'message': msg})
        return Response(serialized_data)







class SafeplaceDetailAPIView_postcode(RetrieveAPIView):
    queryset = Safeplace.objects.all()
    serializer_class = SafeplaceDetailSerializer
    lookup_field = 'postcode'

class SafeplaceDetailAPIView_type(RetrieveAPIView):
    queryset = Safeplace.objects.all()
    serializer_class = SafeplaceDetailSerializer
    lookup_field = 'type'

class SafeplaceUpdateAPIView(UpdateAPIView):
    queryset = Safeplace.objects.all()
    serializer_class = SafeplaceCreateUpdateSerializer
    lookup_field = 'suburb'
    permission_classes = [IsAuthenticated]

class SafeplaceDeleteAPIView(DestroyAPIView):
    queryset = Safeplace.objects.all()
    serializer_class = SafeplaceDetailSerializer
    lookup_field = 'suburb'
