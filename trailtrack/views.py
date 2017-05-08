from rest_framework.generics import ListAPIView
from .models import trailtrack
from .serializers import TrailtrackListSerializer, TrailtrackCreateSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from twilio.rest import Client
import threading
import datetime
""" IMPORTANT, TWILIO ACCOUNT TOKEN WITHOUT THIS SMS WON"T SENT ### """

account_sid = "AC4b6a8c4025120465af4a05a6c948017f"
auth_token = "11557bb09bebac4ee0021cd2bc47b9c3"
client = Client(account_sid, auth_token)

class TrailtrackListAPIView(ListAPIView):
    serializer_class = TrailtrackListSerializer
    def get_queryset(self):
        pass
    def list(self, request, *args, **kwargs):
        deviceid = self.request.query_params.get('deviceid', None) #get deviceid
        if deviceid is not None:
            queryset = trailtrack.objects.filter(deviceid__contains = deviceid).order_by('pk') #filter deviceid by PK
            serializer_class = TrailtrackListSerializer(queryset, many=True)
            serialized_data =  ({'results': serializer_class.data,'status' : status.HTTP_200_OK, 'Message' : 'Filtered by id = ' + deviceid }) #API structure
        else:
            queryset = trailtrack.objects.all().order_by('pk')
            serializer_class = TrailtrackListSerializer(queryset, many=True)
            serialized_data =  ({'results': serializer_class.data,'status' : status.HTTP_200_OK, 'Message' : 'Alldeviceid'}) #API structure

        return  Response(serialized_data)


class TrailtrackCreateSerializer(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView,) :
    serializer_class = TrailtrackCreateSerializer
    def get(self, request): #Get all required paramters from URL
        deviceid = self.request.query_params.get('deviceid', None)
        name = self.request.query_params.get('name', None)
        user_phone_number = self.request.query_params.get('uphone', None)
        contact1 = self.request.query_params.get('c1', None)
        contact2 = self.request.query_params.get('c2', None)
        contact3 = self.request.query_params.get('c3', None)
        status = self.request.query_params.get('status', None)
        period = self.request.query_params.get('period', None)
        lat = self.request.query_params.get('lat', None)
        lng = self.request.query_params.get('lng', None)
        listx = [(lat,lng)]

        ### Calculate Wait Time ###

        seconds = (int(period) * 60) + 60 #converting to mins and adding 1min of respond time.

        #### Checking function by running threading after saving the creation ###

        track = trailtrack.objects.create(deviceid = deviceid, name = name,  user_phone_number = user_phone_number, contact1=contact1, contact2=contact2, contact3=contact3, status=status, period=period, geocode=listx)
        #create objects for attributes
        currentId = track.id #saving the current id to use in threading
        track.save()

        t = threading.Timer(seconds, sendmessage, args =(currentId, )) #Function threading with a timer = sec
        #function send message is at the bottom of the page.
        t.start()
        return Response('Okay')

class TrailtrackUpdateSerializer(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView,):
    serializer_class = TrailtrackCreateSerializer
    def get(self, request): #Get parameters from url.
        deviceid = self.request.query_params.get('deviceid', None)
        status = self.request.query_params.get('status', None)
        lat = self.request.query_params.get('lat', None)
        lng = self.request.query_params.get('lng', None)

        """ THIS FUNCTUON NEEDS FIXING """

        for e in trailtrack.objects.filter(deviceid = deviceid):
            list_1 = e.geocode  #searching for geo
        for e in trailtrack.objects.filter(deviceid = deviceid):
            period = e.period   #searching for period

        """ THIS FUNCTUON NEEDS FIXING """

        list_1.append((lat, lng)) #append tuple of lag and lng within a list
        value = list_1
        # Time Management Schedule
        currentTime = datetime.datetime.now()
        seconds = (int(period) * 60) + 60  #convert sec to min plus the 1min response time
        if lat is not None and lng is not None:
            trailtrack.objects.filter(deviceid = deviceid).update(status=status, geocode=value, updated=currentTime) #creating objects
        else:
            trailtrack.objects.filter(deviceid = deviceid).update(status=status) #creating objects

        ### Main if else
        if status == "reached":  #if status reach, stop the function
            print("You are safe")
        elif status == "safe": #if the status is safe, re run the threading fucntion
            currentUpdate = trailtrack.objects.get(deviceid=deviceid).updated
            g = threading.Timer(seconds, check_update_time, args=(deviceid,  currentUpdate,)) #Compensation 5 seconds
            g.start()
        try:
            return Response('Okay')
        except(ConnectionResetError, TypeError, AttributeError):
            pass


def check_update_time(deviceid, currentUpdateTime): #check for the updatetime
    g = trailtrack.objects.get(deviceid=deviceid).geocode #get into parameters, deviceid and geocode of last location
    g_list = g[len(g)-1] #making the index -1 to get the current index
    lat = g_list[0] #getting lat
    lng = g_list[1]  #getting lng
    c1 = trailtrack.objects.get(deviceid=deviceid).contact1 #getting emergency contact1
    c2 = trailtrack.objects.get(deviceid=deviceid).contact2 #getting emergency contact2
    c3 = trailtrack.objects.get(deviceid=deviceid).contact3 #getting emergency contact3
    name= trailtrack.objects.get(deviceid=deviceid).name
    user_phone = trailtrack.objects.get(deviceid=deviceid).user_phone_number #get use phone number
    present_update_time = trailtrack.objects.get(deviceid=deviceid).updated
    if present_update_time == currentUpdateTime: #if the current time is the same, fire update
        trailtrack.objects.filter(deviceid = deviceid).update(status='Danger') #When the message is send, the status to become danger.
        client.messages.create(to='+'+c1,from_="+61451562589",body="Alert message from " + name + "(" + user_phone + ")." +" I might not be safe. Click the attachment below for my last location.  http://www.google.com/maps/place/" + lat + ',' + lng + "/" )
        client.messages.create(to='+'+c2,from_="+61451562589",body="Alert message from " + name + "(" + user_phone + ")." +" I might not be safe. Click the attachment below for my last location.  http://www.google.com/maps/place/" + lat + ',' + lng + "/" )
        client.messages.create(to='+'+c3,from_="+61451562589",body="Alert message from " + name + "(" + user_phone + ")." +" I might not be safe. Click the attachment below for my last location.  http://www.google.com/maps/place/" + lat + ',' + lng + "/" )
    else:
        print ("You are okay")
### Send Message for Insert Status = Used
def sendmessage (idx):
    #time.sleep(60.0)
    #trailtrack.objects.filter(idx = idx).update(status='Danger')
    g = trailtrack.objects.get(id=idx).geocode  #get into parameters, deviceid and geocode of last location
    g_list = g[len(g)-1] #making the index -1 to get the current index
    lat = g_list[0] #getting lat
    lng = g_list[1] #getting lng
    name= trailtrack.objects.get(id=idx).name
    user_phone = trailtrack.objects.get(id=idx).user_phone_number
    stu = trailtrack.objects.get(id=idx).status
    c1 = trailtrack.objects.get(id=idx).contact1 #getting emergency contact1
    c2 = trailtrack.objects.get(id=idx).contact2 #getting emergency contact2
    c3 = trailtrack.objects.get(id=idx).contact3 #getting emergency contact3
    if stu == "start": #If the timer stops and status is start.
        trailtrack.objects.filter(id = idx).update(status='Danger')
        client.messages.create(to='+'+c1,from_="+61451562589",body="Alert message from " + name + "(" + user_phone + ")." + " I might not be safe. Click the attachment below for my last location.  http://www.google.com/maps/place/" + lat + ',' + lng + "/" )
        client.messages.create(to='+'+c2,from_="+61451562589",body="Alert message from " + name + "(" + user_phone + ")." + " I might not be safe. Click the attachment below for my last location.  http://www.google.com/maps/place/" + lat + ',' + lng + "/" )
        client.messages.create(to='+'+c3,from_="+61451562589",body="Alert message from " + name + "(" + user_phone + ")." + " I might not be safe. Click the attachment below for my last location.  http://www.google.com/maps/place/" + lat + ',' + lng + "/" )
    else:
        pass