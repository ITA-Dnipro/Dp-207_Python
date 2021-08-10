import hashlib
import json
from services.statistics_app.mongo_db_utils.mongo_db_client import client # noqa
from services.statistics_app.mongo_db_utils.transport_app.mongo_models import (
    Route, Car, Train
)


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


def add_hash_to_db_response(db_response):
    '''
    Add route_hash to db_response dict, and return db_response
    '''
    db_response['route_hash'] = dict_hash(db_response)
    #
    return db_response


def save_route_car_in_collection(db_response):
    '''
    Saving route and car in mongodb collections
    '''
    route = Route(
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


def save_route_train_in_collection(db_response):
    '''
    Saving route and car in mongodb collections
    '''
    route = Route(
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


def update_route_car_in_collection(db_response):
    '''
    Updating route and car data in mongodb collections
    '''
    Route.objects(
        departure_name=db_response.get('departure_name'),
        departure_date=db_response.get('departure_date'),
        arrival_name=db_response.get('arrival_name'),
        source_name=db_response.get('source_name'),
    ).update(
        departure_name=db_response.get('departure_name'),
        arrival_name=db_response.get('arrival_name'),
        departure_date=db_response.get('departure_date'),
        parsed_time=db_response.get('parsed_time'),
        source_name=db_response.get('source_name'),
        source_url=db_response.get('source_url'),
        route_hash=db_response.get('route_hash'),
    )
    for car in db_response.get('trips'):
        Car.objects(
            departure_name=car.get('departure_name'),
            departure_date=car.get('departure_date'),
            arrival_name=car.get('arrival_name'),
        ).update(
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


def update_route_train_in_collection(db_response):
    '''
    Updating route and train data in mongodb collections
    '''
    Route.objects(
        departure_name=db_response.get('departure_name'),
        departure_date=db_response.get('departure_date'),
        arrival_name=db_response.get('arrival_name'),
        source_name=db_response.get('source_name'),
    ).update(
        departure_name=db_response.get('departure_name'),
        arrival_name=db_response.get('arrival_name'),
        departure_date=db_response.get('departure_date'),
        parsed_time=db_response.get('parsed_time'),
        source_name=db_response.get('source_name'),
        source_url=db_response.get('source_url'),
        route_hash=db_response.get('route_hash'),
    )
    for train in db_response.get('trips'):
        Train.objects(
            train_number=train.get('train_number'),
            departure_name=train.get('departure_name'),
            departure_date=train.get('departure_date'),
            arrival_name=train.get('arrival_name'),
            arrival_date=train.get('arrival_date'),
        ).update(
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
