from django.conf.urls import url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include, url
from .views import (TrailtrackListAPIView, TrailtrackCreateSerializer,TrailtrackUpdateSerializer)




#import functions into url from views
urlpatterns = [
    url(r'^create/$', TrailtrackCreateSerializer.as_view(), name='create'),
    url(r'^update/$',   TrailtrackUpdateSerializer.as_view(), name='update'),
    # url(r'^(?P<id>[\w-]+)/delete/$', IncidentDeleteAPIView.as_view(), name='delete'),
    # url(r'^(?P<id>[\w-]+)/$', IncidentDetailAPIView.as_view(), name='detail'),
    # url(r'^(?P<id>[\w-]+)/edit/$',   IncidentUpdateAPIView.as_view(), name='update'),
    url(r'^$',   TrailtrackListAPIView.as_view(), name='list'),

]