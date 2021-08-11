from services.statistics_app.mongo_db_utils.mongo_db_client import transport_client, user_client # noqa
from services.statistics_app.mongo_db_utils.transport_app.mongo_models import (
    User
)
import services.statistics_app.mongo_db_utils.transport_app.route_helpers as route_helpers
from mongoengine.errors import DoesNotExist


def is_user_exists_in_mongodb(user_data):
    '''
    Return True if user exists in mongodb
    '''
    user = User.objects(
        username=user_data.get('username'),
        email=user_data.get('email'),
    )
    if user:
        return True
    else:
        return False


def save_user_in_collection(user_data):
    '''
    Saving user data in mongodb collection
    '''
    user = User(
        username=user_data.get('username'),
        first_name=user_data.get('first_name'),
        last_name=user_data.get('last_name'),
        email=user_data.get('email'),
        is_active=user_data.get('is_active'),
        is_staff=user_data.get('is_staff'),
        is_superuser=user_data.get('is_superuser'),
    ).save()
    #
    return user


def get_user_from_collection(user_data):
    '''
    Return User object from mongodb
    '''
    try:
        user = User.objects(
            username=user_data.get('username'),
            email=user_data.get('email'),
        ).get()
        return user
    except DoesNotExist:
        return False


def is_users_route(route_data, route_type):
    '''
    Return User object if Route.user == incoming user data
    '''
    user = get_user_from_collection(user_data=route_data.get('user_data'))
    route = route_helpers.get_route_from_collection(route_data=route_data, route_type=route_type)
    if not user or not route:
        return False
    #
    route_user_id = route.user.id
    user_id = user.id
    #
    if route_user_id == user_id:
        return user
    else:
        return False
