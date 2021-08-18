from django.test import TestCase
from django.http import HttpRequest
from weather.views import main_weather, get_weather_in_city
from django.test import Client

from weather.models import Weather
from hotels.models import City


class WeatherModelTest(TestCase):

    def test_saving_and_retrieving_weather_data(self):
        test_city = City()
        test_city.name = "Kyiv"
        test_city.save()

        city = City.objects.get(name="Kyiv")

        weather = Weather()
        weather.clouds = 0.00
        weather.current_date = "2021-08-12"
        weather.current_temp = 20.66
        weather.description = "clear sky"
        weather.feels_like = 20.48
        weather.humidity = 65.00
        weather.icon = "clear sky"
        weather.max_temp = 25.46
        weather.min_temp = 16.49
        weather.wind = 5.00
        weather.city = city
        weather.save()

        saved_weather = Weather.objects.all()
        self.assertEqual(saved_weather.count(), 1)
