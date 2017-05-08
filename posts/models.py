from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings


class Incident(models.Model):

    #user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)   For user autentication
    deviceid = models.CharField(max_length=50)
    crime = models.CharField(max_length=50)
    crimedesc = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    latitude = models.DecimalField(decimal_places=6, max_digits=9)
    longitude = models.DecimalField(decimal_places=6, max_digits=9)

    def __int__(self):
        return self.crime #return the unit code


    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"id": self.id})
        #return "/posts/incident/%s" %(self.id)


    class Meta:
        ordering = ["-timestamp","-updated"]