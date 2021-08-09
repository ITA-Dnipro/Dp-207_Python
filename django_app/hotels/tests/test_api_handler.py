from django.test import TestCase
from hotels.utils.api_handler import get_data_for_hotels_by_city, get_for_hotel_rooms, CityNotExists, SomeProblemWithParsing
from unittest import mock
from .hotels_api_result import API_RESULT_FOR_HOTELS_IN_THE_CITY, API_RESULT_FOR_HOTELS_ROOMS


CITY = ['Киев', 'Не существующий']

QUERY = {
        "hotel_href": "hotel_href",
        "date_of_departure": "date_of_departure",
        "date_of_arrival": "date_of_arrival"
        }


def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if kwargs['json'] == {"city": CITY[0]}:
        return MockResponse(API_RESULT_FOR_HOTELS_IN_THE_CITY, 200)
    elif kwargs['json'] == {"city": CITY[1]}:
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
        data = get_data_for_hotels_by_city(city=CITY[0])
        self.assertEqual(data, API_RESULT_FOR_HOTELS_IN_THE_CITY)

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_get_data_for_hotels_by_city_with_invalid_city(self, mock):
        with self.assertRaises(CityNotExists):
            get_data_for_hotels_by_city(city=CITY[1])

    @mock.patch('requests.post', side_effect=mocked_requests_post_for_status_code_500)
    def test_get_data_for_hotels_by_city_with_status_code_500(self, mock):
        with self.assertRaises(SomeProblemWithParsing):
            get_data_for_hotels_by_city(city=CITY[0])

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_get_for_hotel_rooms(self, mock):
        data = get_for_hotel_rooms(city=CITY[0], **QUERY)
        self.assertEqual(data, API_RESULT_FOR_HOTELS_ROOMS)

    @mock.patch('requests.post', side_effect=mocked_requests_post_for_status_code_500)
    def test_get_for_hotel_rooms_with_status_code_500(self, mock):
        with self.assertRaises(SomeProblemWithParsing):
            get_for_hotel_rooms(city=CITY[0], **QUERY)
