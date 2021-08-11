from services.statistics_app.mongo_db_utils.mongo_db_client import transport_client, user_client # noqa
import services.statistics_app.mongo_db_utils.transport_app.route_helpers as route_helpers
import services.statistics_app.mongo_db_utils.transport_app.user_helpers as user_helpers
from services.statistics_app.mongo_db_utils.transport_app.mongo_models import (
    Route, Car
)


def save_route_car_in_collection(route_data):
    '''
    Saving route and car in mongodb collections
    '''
    user_data = route_data.get('user_data')
    user_exists = user_helpers.is_user_exists_in_mongodb(user_data=user_data)
    if not user_exists:
        user = user_helpers.save_user_in_collection(user_data=user_data)
    else:
        user = user_helpers.get_user_from_collection(user_data=user_data)
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


def update_route_car_in_collection(route_data):
    '''
    Updating route and car data in mongodb collections
    '''
    user = user_helpers.is_users_route(route_data=route_data, route_type='cars_data')
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
    route = route_helpers.get_route_from_collection(route_data=route_data, route_type='cars_data')
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
