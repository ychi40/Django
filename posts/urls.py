from django.conf.urls import url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include, url
from posts.views import (post_create,post_delete,post_detail,post_list,post_update)




#import functions into url from views
urlpatterns = [
    url(r'^$', post_list, name='list'),
    url(r'^create/$', post_create, name='create'),
    url(r'^(?P<id>\d+)/edit/$', post_update, name='update'),
    url(r'^(?P<id>\d+)/delete/$', post_delete, name='delete'),
    url(r'^(?P<id>\d+)$', post_detail, name='detail'),

]
