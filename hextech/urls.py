"""hextech URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf import settings
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls.static import static
from django.conf.urls import include, url


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^posts/', include("posts.urls", namespace='posts')),
    url(r'^safeplace/', include("api.urls", namespace='safeplace-api')),
    url(r'^api/posts/', include("posts.api.urls", namespace='posts-api')),
    url(r'^api/users/', include("users.urls", namespace='users-api')),
    url(r'^trailtrack/', include("trailtrack.urls", namespace='trails-api')),
]
urlpatterns = format_suffix_patterns(urlpatterns)



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




