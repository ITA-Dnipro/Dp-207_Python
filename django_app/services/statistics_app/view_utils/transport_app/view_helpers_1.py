from services.statistics_app.mongo_db_utils.mongo_db_client import transport_client, user_client # noqa
from services.statistics_app.mongo_db_utils.transport_app.mongo_models import (
    User, Route, Car, Train
)
from mongoengine.errors import DoesNotExist


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


def get_route_data_from_mongodb(user):
    '''
    Return 20 Route objects for specific User
    '''
    routes = Route.objects(user=user)[:20]
    return routes
