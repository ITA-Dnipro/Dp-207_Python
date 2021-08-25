from datetime import datetime
# from subscription.models import WeatherService, TransportService, HotelService
# from subscription.forms import CHOISES
import pytz
import json


class FormServicesHandler():

    def to_object(o):
        print(o)
        form = FormServicesHandler()
        if o.get('weather'):
            form.weather_services = WeatherForm(city=o['city_for_weather'], date_of_expire=o.get('date_of_expire_for_weather'))
        if o.get('hotels'):
            form.hotels_services = HotelForm(city=o['city_for_hotels'], date_of_expire=o.get('date_of_expire_for_hotels'))
            return form
        else:
            return o


class WeatherForm():

    def __init__(self, city, date_of_expire):
        self.city = city
        self.date_of_expire = pytz.utc.localize(datetime.strptime(date_of_expire, '%Y-%m-%d'))


class HotelForm(WeatherForm):
    pass


class TransportForm():

    def __init__(self, city_from, city_to, date_of_expire):
        self.city_from = city_from
        self.city_to = city_to
        self.date_of_expire = date_of_expire


if __name__ == "__main__":
    data = '{"weather": "on", "city_for_weather": "Киев", "date_of_expire_for_weather": "2022-10-20", "hotels": "on", "city_for_hotels": "Киев", "date_of_expire_for_hotels": "2022-10-20"}'
    a = json.loads(data, object_hook=FormServicesHandler.to_object)
    print(a.weather_services.city)
    print(a.hotels_services.city)