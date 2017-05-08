from django import forms

from .models import Incident
#from .models import Crime



class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = [
            "crime",
            "crimedesc",
            "latitude",
            "longitude"


        ]

