import requests

GET_WEATHER_API_URL = "http://flask_weather:5002/appi/get_weather_by_city"


def get_weather_from_api(city):
    """
    Get data from API from Flask
    """
    url = GET_WEATHER_API_URL
    city = {"city_name": city}
    response = requests.post(url, json=city)
    weather = response.json()
    return weather
