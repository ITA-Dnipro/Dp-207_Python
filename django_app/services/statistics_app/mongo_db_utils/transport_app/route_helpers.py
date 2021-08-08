import hashlib
import json
from services.statistics_app.mongo_db_utils.mongo_db_client import client


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


def is_route_exist_in_mongodb(route, route_filter):
    '''
    Check if route exists in mongodb, and return True if exists
    '''
    single_route = route.find_one(filter=route_filter)
    #
    if single_route:
        return True
    else:
        return False


def is_route_hash_differs(route, hash_filter):
    '''
    Check if route_hash differs with route from mongodb
    '''
    found_by_hash = route.find_one(filter=hash_filter)
    #
    if found_by_hash:
        return True
    else:
        return False


def add_hash_to_db_response(db_response):
    '''
    Add route_hash to db_response dict, and return db_response
    '''
    db_response['route_hash'] = dict_hash(db_response)
    #
    return db_response


def get_route_collection():
    '''
    Return route collection object
    '''
    db = client.transport_app
    route = db.route
    #
    route.create_index([("route_hash", 1)], unique=True)
    #
    return route
