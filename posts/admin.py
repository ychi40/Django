from django.contrib import admin

# Register your models here.
from .models import Incident
#from .models import Crime


class IncidentModelAdmin(admin.ModelAdmin):
    list_display = ["crime","updated","timestamp"] #python 3.0 have to change to str
    list_filter = ['timestamp', 'crime']
    search_fields = ['crimedesc']
    class Meta:
        model = Incident

# class CrimeModelAdmin(admin.ModelAdmin):
#     list_display = ["__str__","crimetype"] #python 3.0 have to change to str
#     list_filter = ['crimetype']
#     #list_editable =["crimetype"] #edit link
#     class Meta:
#         model = Crime


admin.site.register(Incident, IncidentModelAdmin)
#admin.site.register(Crime, CrimeModelAdmin)