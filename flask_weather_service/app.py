import requests
import configparser
from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route("/appi/get_weather_by_city", methods=["POST"])
def get_weather_by_city():
    city_name = request.get_json()["city_name"]
    api_key = get_api_key()
    data = get_weather_results(city_name, api_key)
    temp = "{0:.2f}".format(data["main"]["temp"])
    feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    description = data["weather"][0]["description"]
    humidity = "{0:.2f}".format(data["main"]["humidity"])
    wind = "{0:.2f}".format(data["wind"]["speed"])
    clouds = "{0:.2f}".format(data["clouds"]["all"])
    location = data["name"]

    return jsonify({"temp": temp, "feels_like": feels_like,
                    "description": description, "humidity": humidity,
                    "wind": wind, "clouds": clouds, "location": location, "city_name": city_name})


def get_api_key():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config["openweathermap"]["api"]


def get_weather_results(city_name, api_key):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(city_name, api_key)
    r = requests.get(api_url)
    return r.json()


if __name__ == "__main__":
    app.run(debug=True, port=5002, host="0.0.0.0")
