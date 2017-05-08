from django.conf.urls import url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include, url
from .views import (
        IncidentCreateAPIView,
        IncidentDeleteAPIView,
        IncidentDetailAPIView,
        IncidentUpdate,
        IncidentListAPIView,
        IncidentCreateAPIViewNoUser,
)





#import functions into url from views
urlpatterns = [
    url(r'^create/$',   IncidentCreateAPIView.as_view(), name='create'),
    url(r'^createincident/$',   IncidentCreateAPIViewNoUser.as_view(), name='updateincident'),
    url(r'delete/$', IncidentDeleteAPIView.as_view(), name='delete'),
    #url(r'^(?P<id>[\w-]+)/$', IncidentDetailAPIView.as_view(), name='detail'),
    url(r'^update/$',   IncidentUpdate.as_view(), name='update'),
    url(r'^$',   IncidentListAPIView.as_view(), name='list'),

]
