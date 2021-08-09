from django.test import TestCase
from hotels.utils.logic import CityAndHotelsHandler
from .test_api_handler import CITY
from unittest import mock
from .hotels_api_result import API_RESULT_FOR_HOTELS_IN_THE_CITY
from hotels.models import City, Hotel


class TestHotelModel(TestCase):

    @mock.patch('hotels.utils.logic.get_data_for_hotels_by_city', side_effect=API_RESULT_FOR_HOTELS_IN_THE_CITY)
    def test_get_data_from_api_and_create_models(self, mock, city_name=CITY[0]):
        with self.assertRaises(City.DoesNotExist):
            City.objects.get(name=CITY[0])
        instance = CityAndHotelsHandler(city_name)
        instance.get_data_from_api_and_create_models()
        self.assertTrue(City.objects.get(name=CITY[0]))
        self.assertEqual(len(Hotel.objects.all()), 1)

    @mock.patch('hotels.utils.logic.get_data_for_hotels_by_city', side_effect=API_RESULT_FOR_HOTELS_IN_THE_CITY)
    def test_get_data_from_api_and_create_models_with_city_in_db(self, mock, city_name=CITY[0]):
        instance = CityAndHotelsHandler(city_name)
        instance.city.create_city()
        self.assertTrue(City.objects.get(name=CITY[0]))
        instance.get_data_from_api_and_create_models()
        self.assertEqual(len(Hotel.objects.all()), 1)

    @mock.patch('hotels.utils.logic.get_data_for_hotels_by_city', side_effect=API_RESULT_FOR_HOTELS_IN_THE_CITY)
    def test_get_data_from_api_and_create_models_with_city_and_hotel_in_db(self, mock, city_name=CITY[0]):
        instance = CityAndHotelsHandler(city_name)
        city = instance.city.create_city()
        API_RESULT_FOR_HOTELS_IN_THE_CITY[0][0]['city'] = city
        instance.hotel.create_hotel(**API_RESULT_FOR_HOTELS_IN_THE_CITY[0][0])
        self.assertTrue(City.objects.get(name=CITY[0]))
        instance.get_data_from_api_and_create_models()
        self.assertEqual(len(Hotel.objects.all()), 1)
        self.assertEqual(mock.call_count, 0)

    def tearDown(self):
        City.objects.all().delete()
        Hotel.objects.all().delete()


# class TestCreateComment(TestCase):

#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
