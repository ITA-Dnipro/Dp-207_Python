from rest_framework import serializers
from hotels.models import City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['name']