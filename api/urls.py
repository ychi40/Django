from django.conf.urls import url
from django.contrib import admin
from .views import (SafeplaceListAPIView,
                    SafeplaceDetailAPIView,
                    SafeplaceDetailAPIView_type,
                    SafeplaceUpdateAPIView,
                    SafeplaceDeleteAPIView,
                    SafeplaceCreateAPIView,
                    SafeplaceDetailAPIView_postcode)





urlpatterns = [
    url(r'^$', SafeplaceListAPIView.as_view(), name = 'list' ),
    #####
    url(r'^create/$', SafeplaceCreateAPIView.as_view(), name = 'create' ),
    url(r'^location/$', SafeplaceDetailAPIView.as_view(), name='location'),
    url(r'^(?P<suburb>\w+)/$', SafeplaceDetailAPIView.as_view(), name = 'detail'),
    url(r'^(?P<postcode>\w+)/$', SafeplaceDetailAPIView_postcode.as_view(), name = 'postdetail'),
    url(r'^(?P<type>\w+)/$', SafeplaceDetailAPIView_type.as_view(), name='detail'),
    url(r'^(?P<suburb>\w+)/edit/$', SafeplaceUpdateAPIView.as_view(), name = 'update'),
    url(r'^(?P<suburb>\w+)/delete/$', SafeplaceDeleteAPIView.as_view(), name = 'delete'),

]