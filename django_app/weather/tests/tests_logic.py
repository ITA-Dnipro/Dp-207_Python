from django.test import TestCase
from unittest import mock
from weather.utils.logic import WeatherHandler
from weather.test_data.weather_data import CITY, WEATHER_DATA
from hotels.models import City
from weather.models import Weather
from weather.utils.api_handler import get_weather_from_api


class TestWeatherModel(TestCase):

    @mock.patch('weather.utils.logic.get_weather_from_api', side_effect=WEATHER_DATA)
    def test_create_weather_in_city(self, mock, city=CITY['city_name']):
        instance = WeatherHandler(city)
        instance.create_weather_in_city(WEATHER_DATA)
        self.assertTrue(City.objects.get(name=city))
        self.assertEqual(len(Weather.objects.all()), 4)

    # @mock.patch('weather.utils.logic.get_weather_from_api', side_effect=WEATHER_DATA)
    # def test_get_weather_in_city_from_model(self, mock, city=CITY['city_name']):
    #     instance = WeatherHandler(city)
    #     c = instance.get_city_from_city_model()
    #     result = Weather.objects.filter(city=c)
    #     # weather_in_city = instance.get_weather_in_city_from_model()
    #     self.assertEqual(c, city)
    #     # self.assertEqual(weather_in_city[0]['current_date'], '2021-08-12')

    # @mock.patch('weather.utils.logic.get_weather_from_api', side_effect=WEATHER_DATA)
    # def test_create_weather_city_not_in_model(self, mock, city=CITY['city_name']):
    #     instance = WeatherHandler(city)
    #     city = False
    #     instance.create_weather_in_new_city() # doesn't work :(
    #     self.assertTrue(City.objects.get(name=city))
    #     self.assertEqual(len(Weather.objects.all()), 4)

    @mock.patch('weather.utils.logic.get_weather_from_api', side_effect=WEATHER_DATA)
    def test_delete_weather_in_city(self, mock, city=CITY['city_name']):
        instance = WeatherHandler(city)
        instance.delete_weather_in_city()
        self.assertEqual(len(Weather.objects.all()), 0)

    @mock.patch('weather.utils.logic.get_weather_from_api', side_effect=WEATHER_DATA)
    def test_get_city_from_city_model(self, mock, city=CITY['city_name']):
        instance = WeatherHandler(city)
        c = instance.get_city_from_city_model()
        self.assertTrue(City.objects.get(name=c))

    def tearDown(self):
        City.objects.all().delete()
        Weather.objects.all().delete()
