from django.contrib import admin

# Register your models here.
from .models import Safeplace
admin.site.register(Safeplace)



class SafeplaceModelAdmin(admin.ModelAdmin):
    #list_display = ["establishment"] #python 3.0 have to change to str
    list_filter = ['suburb','type']
    search_fields = ['suburb','type']
    class Meta:
        model = Safeplace