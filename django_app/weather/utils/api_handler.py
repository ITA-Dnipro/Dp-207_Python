import requests
import json


def get_weather_from_api(city):
    url = "http://flask_weather:5002/appi/get_weather_by_city"
    city = {"city_name": city}
    response = requests.post(url, json=city)
    data = response.json()
    weather = json.loads(json.dumps(data))
    return weather
