from django.db import models
from jsonfield import JSONField
# Create your models here.
from dirtyfields import DirtyFieldsMixin
class trailtrack(DirtyFieldsMixin,models.Model):
    name = models.CharField(max_length=50)
    deviceid = models.CharField(max_length=50)
    user_phone_number = models.CharField(max_length=50)
    contact1 = models.CharField(max_length=50)
    contact2 = models.CharField(max_length=50)
    contact3 = models.CharField(max_length=50)
    status =  models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    period = models.CharField(max_length=50)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    geocode = JSONField()
    #longitude = JSONField()

    def __int__(self):
        return self.deviceid
        #return the unit code