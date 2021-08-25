from datetime import datetime
from subscription.models import WeatherService, TransportService, HotelService
# from subscription.forms import CHOISES
import pytz
from django.utils import timezone


def find_period(time):
    date_of_expire = datetime.strptime(time, '%Y-%m-%d')
    today = timezone.now()
    period = (pytz.utc.localize(date_of_expire).date() - today.date()).days
    return period


def create_subsciptions(post_dict, user):
    subscriptions = []
    if post_dict.get('weather'):
        subscriptions.append(WeatherServiceHandler().create_subsciption(post_dict, user))
    if post_dict.get('hotels'):
        subscriptions.append(HotelServiceHandler().create_subsciption(post_dict, user))
    if post_dict.get('transport'):
        subscriptions.append(TransportServiceHandler().create_subsciption(post_dict, user))
    return subscriptions


class ServiceHandler():

    def create_subsciption(self, post_dict, user):
        city = post_dict.get(f'city_for_{self.type}')
        date_of_expire = post_dict.get(f'date_of_expire_for_{self.type}')
        date_of_expire = pytz.utc.localize(datetime.strptime(date_of_expire, '%Y-%m-%d'))
        subscription = self.model(city=city, date_of_expire=date_of_expire, user=user).save()
        return subscription


class WeatherServiceHandler(ServiceHandler):

    def __init__(self):
        self.model = WeatherService
        self.type = 'weather'


class HotelServiceHandler(ServiceHandler):

    def __init__(self):
        self.model = HotelService
        self.type = 'hotels'


class TransportServiceHandler():

    def __init__(self):
        self.model = TransportService
        self.type = 'transport'

    def create_subsciption(self, post_dict, user):
        city_of_arrival = post_dict.get('city_of_arrival_for_hotels')
        city_of_departure = post_dict.get('city_of_departure_for_hotels')
        date_of_expire = post_dict.get('date_of_expire_for_hotels')
        date_of_expire = pytz.utc.localize(datetime.strptime(date_of_expire, '%Y-%m-%d'))
        subscription = self.model(city_of_arrival=city_of_arrival, city_of_departure=city_of_departure,  date_of_expire=date_of_expire, user=user).save()
        return subscription
