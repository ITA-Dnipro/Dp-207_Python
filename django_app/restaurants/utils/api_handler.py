import requests

GET_RESTAURANTS_API_URL = "http://flask_restaurants:4800/get_restaurants_by_city/"


def get_restaurants_from_api(city):
    """
    Get data from API from Flask
    """
    url = GET_RESTAURANTS_API_URL
    city = {"city_name": city}
    response = requests.post(url, json=city)
    restaurants = response.json()
    return restaurants