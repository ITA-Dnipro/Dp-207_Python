from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from hotels.models import City
from weather.utils.api_handler import get_weather_from_api
from .serializers import CitySerializer

# Create your views here.

class Cities(APIView):

    def get(self, *args, **kwargs):
        all_cities = City.objects.all()
        serialized_cities = CitySerializer(all_cities, many=True)
        return Response(serialized_cities.data)

    def post(self, request, *args, **kwargs):
        print(request.data)
        data = get_weather_from_api(request.data['city'])
        return Response(data)
