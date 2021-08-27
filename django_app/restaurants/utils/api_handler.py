import requests
import os

GET_RESTAURANTS_API_URL = os.environ.get('GET_RESTAURANTS_API_URL')


def get_restaurants_from_api(city):
    """
    Get data from API from Flask
    """
    url = GET_RESTAURANTS_API_URL
    city = {"city_name": city}
    response = requests.post(url, json=city)
    restaurants = response.json()
    return restaurants