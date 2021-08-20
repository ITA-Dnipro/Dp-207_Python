from django.test import TestCase
from unittest import mock
from weather.utils.logic import WeatherHandler
from weather.test_data.weather_data import CITY, WEATHER_DATA
from hotels.models import City
from weather.models import Weather
from weather.utils.api_handler import get_weather_from_api
from unittest.mock import Mock


class TestWeatherModel(TestCase):

    @mock.patch('weather.utils.logic.WeatherHandler.get_weather_from_api_and_create_model', side_effect=WEATHER_DATA)
    def test_get_weather_from_api_and_create_model(self, mock, city=CITY['city_name']):
        instance = WeatherHandler(city)

        self.assertTrue(instance.get_weather_from_api_and_create_model())

    @mock.patch('weather.utils.logic.WeatherHandler.get_weather_from_api_and_create_model', side_effect=WEATHER_DATA)
    def test_get_city_from_city_model(self, mock, city=CITY['city_name']):
        instance = WeatherHandler(city)
        city_name = instance.get_city_from_city_model()

        self.assertTrue(City.objects.get(name=city_name))

    def tearDown(self):
        City.objects.all().delete()
        Weather.objects.all().delete()
