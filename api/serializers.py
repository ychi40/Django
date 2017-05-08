from rest_framework.serializers import ModelSerializer

from .models import Safeplace

class SafeplaceCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Safeplace
        fields = '__all__'

class SafeplaceDetailSerializer(ModelSerializer):
    class Meta:
        model = Safeplace
        fields = ('__all__')

class SafeplaceListSerializer(ModelSerializer):
    class Meta:
        model = Safeplace
        fields = ('__all__')