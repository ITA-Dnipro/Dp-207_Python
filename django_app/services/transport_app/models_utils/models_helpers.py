from transport.models import Route, Car, Train
from datetime import datetime
import pytz
from django.forms.models import model_to_dict


def is_route_exists(payload):
    '''
    Return True if route exists
    '''
    db_payload = dict(payload)
    db_payload = model_query_time_converter(db_payload)
    route = Route.objects.filter(
        departure_name=db_payload['departure_name'],
        departure_date=db_payload['departure_date'],
        arrival_name=db_payload['arrival_name']
    ).first()
    if route:
        return True
    return False


def is_car_exists(payload):
    '''
    Return True if route exists
    '''
    db_payload = dict(payload)
    db_payload = car_model_query_time_converter(db_payload)
    car = Car.objects.filter(
        departure_name=db_payload['departure_name'],
        departure_date=db_payload['departure_date'],
        arrival_name=db_payload['arrival_name']
    ).first()
    if car:
        return True
    return False


def is_car_has_same_departure_date_with_route(route_departure_date, car):
    '''
    Return True if car has same departure_date with route
    '''
    #
    car_payload = {}
    car_payload['departure_date'] = car['departure_date']
    car_payload = car_model_query_date_converter(
        car_payload
    )
    #
    route_payload = {}
    route_payload['departure_date'] = route_departure_date
    route_payload = model_query_time_converter(
        route_payload
    )
    #
    route_date = route_payload['departure_date']
    car_date = car_payload['departure_date']
    #
    if route_date == car_date:
        return True
    return False


def save_api_response_in_route_and_train_models(api_response):
    '''
    Saving api_response dict in Route and Train models
    '''
    route = Route.objects.create(
        departure_name=api_response['departure_name'],
        departure_date=api_response['departure_date'],
        arrival_name=api_response['arrival_name'],
        parsed_time=api_response['parsed_time'],
        source_name=api_response['source_name'],
        source_url=api_response['source_url'],
    )
    for train in api_response['trips']:
        Train.objects.create(
            route_id=route,
            train_name=train['train_name'],
            train_number=train['train_number'],
            train_uid=train['train_number'],
            departure_name=train['departure_name'],
            departure_code=train['departure_code'],
            departure_date=train['departure_date'],
            arrival_name=train['arrival_name'],
            arrival_code=train['arrival_code'],
            arrival_date=train['arrival_date'],
            in_route_time=train['in_route_time'],
            parsed_time=train['parsed_time'],
            source_name=train['source_name'],
            source_url=train['source_url'],
        )


def save_api_response_in_route_and_car_models(api_response):
    '''
    Saving api_response dict in Route and Car models
    '''
    route = Route.objects.create(
        departure_name=api_response['departure_name'],
        departure_date=api_response['departure_date'],
        arrival_name=api_response['arrival_name'],
        parsed_time=api_response['parsed_time'],
        source_name=api_response['source_name'],
        source_url=api_response['source_url'],
    )
    for one_car in api_response['trips']:
        payload = {
            'departure_name': one_car['departure_name'],
            'departure_date': one_car['departure_date'],
            'arrival_name': one_car['arrival_name'],
        }
        car = is_car_exists(payload)
        #
        same_car_and_route_derarture_date = (
            is_car_has_same_departure_date_with_route(
                route_departure_date=api_response['departure_date'],
                car=one_car
            )
        )
        if not car and same_car_and_route_derarture_date:
            Car.objects.create(
                route_id=route,
                departure_name=one_car['departure_name'],
                departure_date=one_car['departure_date'],
                arrival_name=one_car['arrival_name'],
                price=one_car['price'],
                car_model=one_car['car_model'],
                blablacar_url=one_car['blablacar_url'],
                parsed_time=one_car['parsed_time'],
                source_name=one_car['source_name'],
                source_url=one_car['source_url'],
            )


def model_query_time_converter(db_payload):
    '''
    Return payload dict with payload['departure_date'] converted
    to datetime object with proper timezone
    '''
    db_payload['departure_date'] = datetime.strptime(
        db_payload['departure_date'], '%d.%m.%Y'
    )
    db_payload['departure_date'] = pytz.timezone(
        'Europe/Kiev'
    ).localize(
        db_payload['departure_date'], is_dst=True
    )
    db_payload['departure_date'] = (
        db_payload['departure_date'].astimezone(pytz.timezone('UTC'))
    )
    return db_payload


def car_model_query_time_converter(db_payload):
    '''
    Return payload dict with payload['departure_date'] converted
    to datetime object with proper timezone
    '''
    db_payload['departure_date'] = datetime.strptime(
        db_payload['departure_date'], '%d/%m/%Y %H:%M:%S'
    )
    db_payload['departure_date'] = pytz.timezone(
        'Europe/Kiev'
    ).localize(
        db_payload['departure_date'], is_dst=True
    )
    db_payload['departure_date'] = (
        db_payload['departure_date'].astimezone(pytz.timezone('UTC'))
    )
    return db_payload


def car_model_query_date_converter(db_payload):
    '''
    Return payload dict with payload['departure_date'] converted
    to datetime object with just date
    '''
    db_payload['departure_date'] = datetime.strptime(
        db_payload['departure_date'], '%d/%m/%Y %H:%M:%S'
    )
    db_payload['departure_date'] = db_payload['departure_date'].replace(
        hour=0,
        minute=0,
        second=0
    )
    db_payload['departure_date'] = pytz.timezone(
        'Europe/Kiev'
    ).localize(
        db_payload['departure_date'], is_dst=True
    )
    db_payload['departure_date'] = (
        db_payload['departure_date'].astimezone(pytz.timezone('UTC'))
    )
    return db_payload


def get_cars_db_data(payload):
    db_payload = dict(payload)
    db_payload = model_query_time_converter(db_payload)
    route = Route.objects.filter(
        departure_name=db_payload['departure_name'],
        departure_date=db_payload['departure_date'],
        arrival_name=db_payload['arrival_name'],
        source_name='poezdato/blablacar',
    ).first()
    #
    if not route:
        db_response = {}
        db_response['result'] = False
        return db_response
    #
    db_response = model_to_dict(route)
    cars = [
        car for car in Car.objects.filter(
            route_id=route,
        ).all().values()
    ]
    db_response['trips'] = cars
    db_response['result'] = True
    return db_response


def get_trains_db_data(payload):
    db_payload = dict(payload)
    db_payload = model_query_time_converter(db_payload)
    route = Route.objects.filter(
        departure_name=db_payload['departure_name'],
        departure_date=db_payload['departure_date'],
        arrival_name=db_payload['arrival_name'],
        source_name='poezd.ua',
    ).first()
    #
    if not route:
        db_response = {}
        db_response['result'] = False
        return db_response
    #
    db_response = model_to_dict(route)
    trains = [
        train for train in Train.objects.filter(route_id=route).all().values()
    ]
    db_response['trips'] = trains
    db_response['result'] = True
    return db_response
