import hashlib
import json
from services.statistics_app.mongo_db_utils.mongo_db_client import transport_client, user_client # noqa
from services.statistics_app.mongo_db_utils.transport_app.mongo_models import (
    Route, Car, Train, User
)
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


def add_hash_to_db_response(db_response):
    '''
    Add route_hash to db_response dict, and return db_response
    '''
    db_response['route_hash'] = dict_hash(db_response)
    #
    return db_response


def save_route_car_in_collection(route_data):
    '''
    Saving route and car in mongodb collections
    '''
    user_data = route_data.get('user_data')
    user_exists = is_user_exists_in_mongodb(user_data=user_data)
    if not user_exists:
        user = save_user_in_collection(user_data=user_data)
    else:
        user = get_user_from_collection(user_data=user_data)
    #
    db_response = route_data.get('cars_data')
    route = Route(
        user=user,
        departure_name=db_response.get('departure_name'),
        arrival_name=db_response.get('arrival_name'),
        departure_date=db_response.get('departure_date'),
        parsed_time=db_response.get('parsed_time'),
        source_name=db_response.get('source_name'),
        source_url=db_response.get('source_url'),
        route_hash=db_response.get('route_hash'),
    ).save()
    for car in db_response.get('trips'):
        Car(
            route=route,
            departure_name=car.get('departure_name'),
            departure_date=car.get('departure_date'),
            arrival_name=car.get('arrival_name'),
            price=car.get('price'),
            car_model=car.get('car_model'),
            blablacar_url=car.get('blablacar_url'),
            parsed_time=car.get('parsed_time'),
            source_name=car.get('source_name'),
            source_url=car.get('source_url'),
        ).save()


def save_route_train_in_collection(route_data):
    '''
    Saving route and car in mongodb collections
    '''
    user_data = route_data.get('user_data')
    user_exists = is_user_exists_in_mongodb(user_data=user_data)
    if not user_exists:
        user = save_user_in_collection(user_data=user_data)
    else:
        user = get_user_from_collection(user_data=user_data)
    db_response = route_data.get('trains_data')
    route = Route(
        user=user,
        departure_name=db_response.get('departure_name'),
        arrival_name=db_response.get('arrival_name'),
        departure_date=db_response.get('departure_date'),
        parsed_time=db_response.get('parsed_time'),
        source_name=db_response.get('source_name'),
        source_url=db_response.get('source_url'),
        route_hash=db_response.get('route_hash'),
    ).save()
    for train in db_response.get('trips'):
        Train(
            route=route,
            #
            train_name=train.get('train_name'),
            train_number=train.get('train_number'),
            train_uid=train.get('train_uid'),
            #
            departure_name=train.get('departure_name'),
            departure_code=train.get('departure_code'),
            departure_date=train.get('departure_date'),
            #
            arrival_name=train.get('arrival_name'),
            arrival_code=train.get('arrival_code'),
            arrival_date=train.get('arrival_date'),
            #
            in_route_time=train.get('in_route_time'),
            parsed_time=train.get('parsed_time'),
            source_name=train.get('source_name'),
            source_url=train.get('source_url'),
        ).save()


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


def get_route_from_collection(route_data, route_type):
    '''
    Return Route object
    '''
    db_response = route_data.get(route_type)
    user = get_user_from_collection(user_data=route_data.get('user_data'))
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


def is_users_route(route_data, route_type):
    '''
    Return User object if Route.user == incoming user data
    '''
    user = get_user_from_collection(user_data=route_data.get('user_data'))
    route = get_route_from_collection(route_data=route_data, route_type=route_type)
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


def update_route_car_in_collection(route_data):
    '''
    Updating route and car data in mongodb collections
    '''
    user = is_users_route(route_data=route_data, route_type='cars_data')
    if not user:
        return save_route_car_in_collection(route_data=route_data)
    #
    db_response = route_data.get('cars_data')
    route = Route.objects(
        user=user,
        departure_name=db_response.get('departure_name'),
        departure_date=db_response.get('departure_date'),
        arrival_name=db_response.get('arrival_name'),
        source_name=db_response.get('source_name'),
    ).update(
        user=user,
        departure_name=db_response.get('departure_name'),
        arrival_name=db_response.get('arrival_name'),
        departure_date=db_response.get('departure_date'),
        parsed_time=db_response.get('parsed_time'),
        source_name=db_response.get('source_name'),
        source_url=db_response.get('source_url'),
        route_hash=db_response.get('route_hash'),
    )
    route = get_route_from_collection(route_data=route_data, route_type='cars_data')
    for car in db_response.get('trips'):
        Car.objects(
            route=route,
            departure_name=car.get('departure_name'),
            departure_date=car.get('departure_date'),
            arrival_name=car.get('arrival_name'),
        ).update(
            route=route,
            departure_name=car.get('departure_name'),
            departure_date=car.get('departure_date'),
            arrival_name=car.get('arrival_name'),
            price=car.get('price'),
            car_model=car.get('car_model'),
            blablacar_url=car.get('blablacar_url'),
            parsed_time=car.get('parsed_time'),
            source_name=car.get('source_name'),
            source_url=car.get('source_url'),
            upsert=True
        )


def update_route_train_in_collection(route_data):
    '''
    Updating route and train data in mongodb collections
    '''
    user = is_users_route(route_data=route_data, route_type='trains_data')
    if not user:
        return save_route_train_in_collection(route_data=route_data)
    #
    db_response = route_data.get('trains_data')
    Route.objects(
        user=user,
        departure_name=db_response.get('departure_name'),
        departure_date=db_response.get('departure_date'),
        arrival_name=db_response.get('arrival_name'),
        source_name=db_response.get('source_name'),
    ).update(
        user=user,
        departure_name=db_response.get('departure_name'),
        arrival_name=db_response.get('arrival_name'),
        departure_date=db_response.get('departure_date'),
        parsed_time=db_response.get('parsed_time'),
        source_name=db_response.get('source_name'),
        source_url=db_response.get('source_url'),
        route_hash=db_response.get('route_hash'),
    )
    route = get_route_from_collection(route_data=route_data, route_type='trains_data')
    for train in db_response.get('trips'):
        Train.objects(
            route=route,
            train_number=train.get('train_number'),
            departure_name=train.get('departure_name'),
            departure_date=train.get('departure_date'),
            arrival_name=train.get('arrival_name'),
            arrival_date=train.get('arrival_date'),
        ).update(
            route=route,
            train_name=train.get('train_name'),
            train_number=train.get('train_number'),
            train_uid=train.get('train_uid'),
            #
            departure_name=train.get('departure_name'),
            departure_code=train.get('departure_code'),
            departure_date=train.get('departure_date'),
            #
            arrival_name=train.get('arrival_name'),
            arrival_code=train.get('arrival_code'),
            arrival_date=train.get('arrival_date'),
            #
            in_route_time=train.get('in_route_time'),
            parsed_time=train.get('parsed_time'),
            source_name=train.get('source_name'),
            source_url=train.get('source_url'),
            upsert=True,
        )
