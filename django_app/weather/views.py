from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import requests
from .forms import WeatherForm
import datetime

from .utils.api_handler import get_weather_from_api


def main_weather(request):
    return render(request, 'weather/main_weather.html', {})


def get_weather_in_city(request):
    if request.method == "POST":
        city = request.POST.get("city")
        weather_in_city = get_weather_from_api(city)
        current_date = datetime.datetime.now().date()
        form = WeatherForm()
        return render(request, "weather/weather_results.html",
                      {"weather_info": weather_in_city,
                       "form": form, "current_date": current_date, })
