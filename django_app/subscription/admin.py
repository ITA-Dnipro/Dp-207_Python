from django.contrib import admin
from .models import WeatherService, HotelService

admin.site.register([WeatherService, HotelService])
