from flask import Flask
from .parser import ScraperForRestaurants


app = Flask(__name__)

@app.route("/", methods=["POST"])
def get_restaurants_by_city():
    data = ScraperForRestaurants()
    result = data.get_content("dnepr")
    #temperature = "{0:.2f}".format(data["main"]["temp"])
    #feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    #description = data["weather"][0]["description"]
    #humidity = "{0:.2f}".format(data["main"]["humidity"])
    #wind = "{0:.2f}".format(data["wind"]["speed"])
    #clouds = "{0:.2f}".format(data["clouds"]["all"])
    #location = data["name"]

    return "hello"



if __name__ == '__main__':
    app.run(Debug=True, port='4100', host='0.0.0.0')