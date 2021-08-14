from services.statistics_app.mongo_db_utils.mongo_db_client import transport_client, user_client # noqa
from services.statistics_app.mongo_db_utils.transport_app.mongo_models import (
    User, Route, Car, Train
)
from mongoengine.errors import DoesNotExist
from datetime import datetime
import pytz


def get_users_count():
    '''
    Return count how many users in mongodb
    '''
    return User.objects.count()


def get_routes_count(username):
    '''
    Return count how many routes in mongodb
    '''
    user = get_user(username=username)
    return Route.objects(user=user).count()


def get_last_20_users():
    '''
    Return last 20 users from mongodb
    '''
    users = User.objects[:20]
    return users


def get_user(username):
    '''
    Return User object from mongodb by username
    '''
    try:
        user = User.objects(username=username).get()
        return user
    except DoesNotExist:
        return None


def get_20_routes_from_mongodb(user):
    '''
    Return 20 Route objects for specific User
    '''
    routes = Route.objects(user=user)[:20]
    return routes


def payload_datetime_converter(payload):
    '''
    Return datetime object for payload
    '''
    payload['departure_date'] = datetime.strptime(
        payload['departure_date'], '%d.%m.%Y'
    ).replace(hour=0, minute=0, second=0)
    payload['departure_date'] = pytz.timezone('Europe/Kiev').localize(
        payload['departure_date'], is_dst=True
    )
    payload['departure_date'] = (
        payload['departure_date'].astimezone(pytz.timezone('UTC'))
    )
    #
    return payload


def get_route_data(username, payload):
    '''
    Return Route statistics data
    '''
    user = get_user(username=username)
    if payload.get('transport_types') == 'car':
        payload['source_name'] = 'poezdato/blablacar'
    elif payload.get('transport_types') == 'train':
        payload['source_name'] = 'poezd.ua'
    #
    payload = payload_datetime_converter(payload=payload)
    try:
        route = Route.objects(
            user=user,
            departure_name=payload.get('departure_name'),
            departure_date=payload.get('departure_date'),
            arrival_name=payload.get('arrival_name'),
            source_name=payload.get('source_name')
        ).get()
        return route
    except DoesNotExist:
        return None


def get_route_stats(route):
    '''
    Return dict with additional statistics of route
    '''
    if route.source_name == 'poezdato/blablacar':
        return get_route_cars_stats(route=route)
    elif route.source_name == 'poezd.ua':
        return get_route_trains_stats(route=route)


def get_route_cars_stats(route):
    '''
    Return result_dict with Route Cars statistics
    '''
    result_dict = {}
    #
    cars_count = Car.objects(route=route).count()
    cars = Car.objects(route=route).all()
    #
    cars_prices = [float(car.price.split(' ')[0]) for car in cars]
    cars_min_price = int(min(cars_prices))
    cars_max_price = int(max(cars_prices))
    cars_avg_price = sum(cars_prices) / len(cars_prices)
    #
    result_dict['cars_count'] = cars_count
    result_dict['cars_min_price'] = f'{cars_min_price} UAH'
    result_dict['cars_max_price'] = f'{cars_max_price} UAH'
    result_dict['cars_avg_price'] = f'{cars_avg_price} UAH'
    #
    return result_dict


def get_route_trains_stats(route):
    '''
    Return result_dict with Route Trains statistics
    '''
    result_dict = {}
    trains_count = Train.objects(route=route).count()
    trains = Train.objects(route=route).all()
    trains_in_route_times = [{train.id: {'original': train.in_route_time}} for train in trains]
    in_route_data = train_in_route_time_data(trains=trains_in_route_times)
    #
    result_dict['trains_count'] = trains_count
    #
    result_dict['min_in_route_time'] = in_route_data.get('min_in_route_time')
    result_dict['max_in_route_time'] = in_route_data.get('max_in_route_time')
    result_dict['avg_in_route_time'] = in_route_data.get('avg_in_route_time')
    return result_dict


def train_in_route_time_data(trains):
    '''
    Return list of trains in_route_times converted in seconds
    '''
    result_dict = {}

    for train in trains:
        for key, value in train.items():
            original_time = value.get('original')
            hours = original_time.split('ч')[0].strip()
            minutes = original_time.split('ч')[1].split('мин')[0].strip()
            train_seconds = hours_minutes_to_seconds_converter(hours=hours, minutes=minutes)
            train[key] = {'original': original_time, 'seconds': train_seconds}
    #
    list_of_sec = [list(train.values()) for train in trains]
    list_of_sec = [train[0].get('seconds') for train in list_of_sec]
    min_in_route_time = min(list_of_sec)
    max_in_route_time = max(list_of_sec)
    avg_in_route_time = sum(list_of_sec) / len(list_of_sec)
    #
    min_in_route_time = seconds_to_hours_and_minutes_converter(seconds=min_in_route_time)
    max_in_route_time = seconds_to_hours_and_minutes_converter(seconds=max_in_route_time)
    avg_in_route_time = seconds_to_hours_and_minutes_converter(seconds=avg_in_route_time)
    #
    result_dict['min_in_route_time'] = min_in_route_time
    result_dict['max_in_route_time'] = max_in_route_time
    result_dict['avg_in_route_time'] = avg_in_route_time
    return result_dict


def hours_minutes_to_seconds_converter(hours, minutes):
    '''
    Return seconds out of hours and minutes
    '''
    return int(hours) * 3600 + int(minutes) * 60


def seconds_to_hours_and_minutes_converter(seconds):
    '''
    Return x hours n minues out of seconds
    '''
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f'{int(hours)} ч {int(minutes)} мин'
