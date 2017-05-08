from rest_framework.serializers import ModelSerializer

from .models import trailtrack


class TrailtrackListSerializer(ModelSerializer):
    class Meta:
        model = trailtrack
        fields =[
            'id',
            'name',
            'user_phone_number',
            'deviceid',
            'contact1',
            'contact2',
            'contact3',
            'period',
            'geocode',
            'status',
        ]

class TrailtrackCreateSerializer(ModelSerializer):
    class Meta:
        model = trailtrack
        fields =[
            'id',
            'name',
            'user_phone_number',
            'deviceid',
            'contact1',
            'contact2',
            'contact3',
            'period',
            'geocode',
            'status',
        ]

class TrailtrackUpdateSerializer(ModelSerializer):
    class Meta:
        model = trailtrack
        fields =[
            'id',
            'name',
            'user_phone_number',
            'deviceid',
            'contact1',
            'contact2',
            'contact3',
            'period',
            'geocode',
            'status',
        ]
