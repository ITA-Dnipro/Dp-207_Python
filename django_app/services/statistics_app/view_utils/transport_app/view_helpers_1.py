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
    if len(payload.get('transport_types')) >= 2:
        return None
    #
    user = get_user(username=username)
    for tr in payload.get('transport_types'):
        if tr == 'car':
            payload['source_name'] = 'poezdato/blablacar'
        elif tr == 'train':
            payload['source_name'] = 'poezd.ua'
        else:
            payload['source_name'] = None
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
