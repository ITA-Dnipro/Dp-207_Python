from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import WeatherForm
from .utils.logic import WeatherHandler
from django.conf import settings
from django.core.cache import cache


CACHE_TTL = getattr(settings, 'CACHE_TTL', settings.SESSION_EXPIRATION)
CACHE_KEY = 'weather'

def main_weather(request):

    """Display the main page with a form to fill in the city name"""

    return render(request, 'weather/main_weather.html', {})


def get_weather_in_city(request):

    """
    Display the result page with the current weather in the city provided by
    the user's input. If the city does not exist, the warning message is displayed.
    Then, the main page with the form is shown instead of the result page
    """

    if request.method == "POST":
        city = request.POST.get("city").capitalize()
        weather_object = WeatherHandler(city)

        if not weather_object.get_weather_from_api_and_create_model():
            messages.warning(request, 'City does not exist!')
            return redirect('weather:main')

        elif CACHE_KEY in cache:
            weather_in_city = cache.get(CACHE_KEY)
            form = WeatherForm()
            return render(request, "weather/weather_results.html",
                          {"weather_info": weather_in_city,
                           "form": form, "city": city})
        else:
            weather_in_city = weather_object.get_weather_from_model()
            cache.set(CACHE_KEY, weather_in_city, timeout=CACHE_TTL)
            form = WeatherForm()
            return render(request, "weather/weather_results.html",
                          {"weather_info": weather_in_city,
                           "form": form, "city": city})
