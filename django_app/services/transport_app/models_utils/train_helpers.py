from transport.models import Route, Train
from django.forms.models import model_to_dict
from services.transport_app.models_utils.route_helpers import (
    model_query_time_converter
)
from datetime import datetime
import pytz
from services.transport_app.api_utils.api_response_helpers import (
    train_api_response_time_converter
)
from services.statistics_app.celery_utils.celery_tasks.transport_app.transport_tasks_1 import (
    save_trains_db_data_to_mongo_db
)


def save_api_response_in_route_and_train_models(api_response):
    '''
    Saving api_response dict in Route and Train models
    '''
    api_response = train_api_response_time_converter(api_response)
    #
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


def update_api_response_in_route_and_train_models(api_response, source_name):
    '''
    Update Route and Train models rows
    '''
    #
    api_response = train_api_response_time_converter(api_response)
    #
    Route.objects.filter(
        departure_name=api_response['departure_name'],
        departure_date=api_response['departure_date'],
        arrival_name=api_response['arrival_name'],
        source_name=source_name
    ).update(
        departure_name=api_response['departure_name'],
        departure_date=api_response['departure_date'],
        arrival_name=api_response['arrival_name'],
        parsed_time=api_response['parsed_time'],
        source_name=api_response['source_name'],
        source_url=api_response['source_url'],
    )
    #
    route = Route.objects.filter(
        departure_name=api_response['departure_name'],
        departure_date=api_response['departure_date'],
        arrival_name=api_response['arrival_name'],
        source_name=source_name
    ).first()
    for train in api_response['trips']:
        db_train = Train.objects.filter(
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
            source_name=train['source_name'],
            source_url=train['source_url'],
        )
        if db_train.exists():
            db_train.update(
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
        else:
            db_train.create(
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


def get_trains_db_data(payload, source_name):
    db_payload = dict(payload)
    db_payload = model_query_time_converter(db_payload)
    route = Route.objects.filter(
        departure_name=db_payload['departure_name'],
        departure_date=db_payload['departure_date'],
        arrival_name=db_payload['arrival_name'],
        source_name=source_name,
    ).first()
    #
    if not route:
        db_response = {}
        db_response['result'] = False
        return db_response
    #
    db_response = model_to_dict(route)
    #
    now_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
    #
    trains = [
        train for train in Train.objects.filter(
            route_id=route
        ).filter(
            departure_date__gte=now_utc
        ).order_by(
            'departure_date'
        ).all().values()
    ]
    db_response['trips'] = trains
    db_response['result'] = True
    #
    save_trains_db_data_to_mongo_db.delay(db_response=db_response)
    #
    return db_response
