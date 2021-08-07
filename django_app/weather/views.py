from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import WeatherForm
from .utils.logic import WeatherHandler


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
        if not weather_object.create_weather_in_new_city():
            messages.warning(request, 'City does not exist!')
            return redirect('weather:main')

        weather_in_city = weather_object.get_weather_in_city_from_model()
        form = WeatherForm()
        return render(request, "weather/weather_results.html", {"weather_info": weather_in_city,
                                                                "form": form, "city": city})
