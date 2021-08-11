import hashlib
import json
from services.statistics_app.mongo_db_utils.mongo_db_client import transport_client, user_client # noqa
from services.statistics_app.mongo_db_utils.transport_app.mongo_models import (
    Route
)
import services.statistics_app.mongo_db_utils.transport_app.user_helpers as user_helpers
from mongoengine.errors import DoesNotExist, ValidationError


def dict_hash(dictionary):
    '''
    Return string with MD5 hash of a dictionary
    '''
    dhash = hashlib.md5()
    #
    encoded = json.dumps(dictionary, sort_keys=True).encode()
    dhash.update(encoded)
    #
    return dhash.hexdigest()


def add_hash_to_db_response(db_response):
    '''
    Add route_hash to db_response dict, and return db_response
    '''
    db_response['route_hash'] = dict_hash(db_response)
    #
    return db_response


def is_route_exist_in_mongodb(db_response):
    '''
    Check if route exists in mongodb, and return True if exists
    '''
    single_route = Route.objects(
        departure_name=db_response.get('departure_name'),
        departure_date=db_response.get('departure_date'),
        arrival_name=db_response.get('arrival_name'),
        source_name=db_response.get('source_name'),
    )
    #
    if single_route:
        return True
    else:
        return False


def is_route_hash_differs(db_response):
    '''
    Check if route_hash differs with route from mongodb
    '''
    found_by_hash = Route.objects(
        route_hash=db_response.get('route_hash'),
    )
    #
    if found_by_hash:
        return True
    else:
        return False


def get_route_from_collection(route_data, route_type):
    '''
    Return Route object
    '''
    db_response = route_data.get(route_type)
    user = user_helpers.get_user_from_collection(user_data=route_data.get('user_data'))
    try:
        route = Route.objects(
            user=user,
            departure_name=db_response.get('departure_name'),
            departure_date=db_response.get('departure_date'),
            arrival_name=db_response.get('arrival_name'),
            source_name=db_response.get('source_name'),
        ).get()
        #
        return route
    except (DoesNotExist, ValidationError):
        return False
