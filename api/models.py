from django.db import models

# Create your models here.
class Safeplace(models.Model):
    establishment = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    suburb = models.CharField(max_length=250)
    postcode = models.IntegerField()
    state = models.CharField(max_length=250)
    type = models.CharField(max_length=250)
    latitude = models.DecimalField(decimal_places=6,max_digits=10)
    longitude =  models.DecimalField(decimal_places=6,max_digits=10)


    def __str__(self):
        return 'Safeplace: {} {}'.format(self.establishment, self.type) # return the unit code