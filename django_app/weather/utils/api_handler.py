import requests
import os

GET_WEATHER_API_URL = os.environ.get('GET_WEATHER_API_URL')


def get_weather_from_api(city: object) -> object:
    """
    Get data from API from Flask
    """
    url = GET_WEATHER_API_URL
    city = {"city_name": city}
    response = requests.post(url, json=city)
    weather = response.json()
    return weather
