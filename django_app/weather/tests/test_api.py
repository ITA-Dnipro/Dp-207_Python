from django.test import TestCase
from unittest import mock

from weather.utils.api_handler import get_weather_from_api
from weather.test_data.weather_data import CITY, WEATHER_DATA


class ApiHandlerTest(TestCase):
    @mock.patch("weather.utils.api_handler.requests.post")
    def test_call_api(self, mock_post):
        my_mock_response = mock.Mock(status_code=200)
        my_mock_response.json.return_value = {"result": [WEATHER_DATA]}
        mock_post.return_value = my_mock_response
        response = get_weather_from_api(city=CITY['city_name'])
        agent_data = response["result"][0]['forecast'][0]
        self.assertEqual(agent_data["current_date"], "2021-08-12")
