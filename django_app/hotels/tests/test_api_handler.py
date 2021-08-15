from django.test import TestCase
from hotels.utils.api_handler import get_data_for_hotels_by_city, get_for_hotel_rooms, CityNotExists, SomeProblemWithParsing
from unittest import mock
from .fixture import API_RESULT_FOR_HOTELS_IN_THE_CITY, API_RESULT_FOR_HOTELS_ROOMS, CITY_EXISTS, CITY_NOT_EXIST, QUERY


def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if kwargs['json'] == {"city": CITY_EXISTS}:
        return MockResponse(API_RESULT_FOR_HOTELS_IN_THE_CITY, 200)
    elif kwargs['json'] == {"city": CITY_NOT_EXIST}:
        return MockResponse({"msg": "Such city doesn't exist"}, 404)
    elif kwargs['json'] == QUERY:
        return MockResponse(API_RESULT_FOR_HOTELS_ROOMS, 200)


def mocked_requests_post_for_status_code_500(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data
    return MockResponse({"msg": "Some problem with parser. Try later"}, 500)


class TestApiHandler(TestCase):

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_get_data_for_hotels_by_city_with_valid_city(self, mock):
        data = get_data_for_hotels_by_city(city=CITY_EXISTS)
        self.assertEqual(data, API_RESULT_FOR_HOTELS_IN_THE_CITY)

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_get_data_for_hotels_by_city_with_invalid_city(self, mock):
        with self.assertRaises(CityNotExists):
            get_data_for_hotels_by_city(city=CITY_NOT_EXIST)

    @mock.patch('requests.post', side_effect=mocked_requests_post_for_status_code_500)
    def test_get_data_for_hotels_by_city_with_status_code_500(self, mock):
        with self.assertRaises(SomeProblemWithParsing):
            get_data_for_hotels_by_city(city=CITY_EXISTS)

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_get_for_hotel_rooms(self, mock):
        data = get_for_hotel_rooms(city=CITY_EXISTS, **QUERY)
        self.assertEqual(data, API_RESULT_FOR_HOTELS_ROOMS)

    @mock.patch('requests.post', side_effect=mocked_requests_post_for_status_code_500)
    def test_get_for_hotel_rooms_with_status_code_500(self, mock):
        with self.assertRaises(SomeProblemWithParsing):
            get_for_hotel_rooms(city=CITY_EXISTS, **QUERY)
