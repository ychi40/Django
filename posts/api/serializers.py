from rest_framework.serializers import ModelSerializer

from ..models import Incident


class IncidentListSerializer(ModelSerializer):
    class Meta:
        model = Incident
        fields =[
            'id',
            'deviceid',
            #'user',
            'crime',
            'crimedesc',
            'latitude',
            'longitude',
        ]



class IncidentDetailSerializer(ModelSerializer):
    class Meta:
        model = Incident
        fields =[
            'id',
            'deviceid',
           # 'user',
            'crime',
            'crimedesc',
            'latitude',
            'longitude',
        ]



class IncidentCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Incident
        fields =[
            'id',
            'deviceid',
            'crime',
            'crimedesc',
            'latitude',
            'longitude',
        ]


