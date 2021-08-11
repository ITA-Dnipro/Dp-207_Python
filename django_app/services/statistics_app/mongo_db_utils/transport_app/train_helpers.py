from services.statistics_app.mongo_db_utils.mongo_db_client import transport_client, user_client # noqa
import services.statistics_app.mongo_db_utils.transport_app.user_helpers as user_helpers
import services.statistics_app.mongo_db_utils.transport_app.route_helpers as route_helpers
from services.statistics_app.mongo_db_utils.transport_app.mongo_models import (
    Route, Train
)


def save_route_train_in_collection(route_data):
    '''
    Saving route and car in mongodb collections
    '''
    user_data = route_data.get('user_data')
    user_exists = user_helpers.is_user_exists_in_mongodb(user_data=user_data)
    if not user_exists:
        user = user_helpers.save_user_in_collection(user_data=user_data)
    else:
        user = user_helpers.get_user_from_collection(user_data=user_data)
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


def update_route_train_in_collection(route_data):
    '''
    Updating route and train data in mongodb collections
    '''
    user = user_helpers.is_users_route(route_data=route_data, route_type='trains_data')
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
    route = route_helpers.get_route_from_collection(route_data=route_data, route_type='trains_data')
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
