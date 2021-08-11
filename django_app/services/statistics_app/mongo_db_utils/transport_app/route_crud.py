from services.statistics_app.mongo_db_utils.transport_app.car_helpers import (
    save_route_car_in_collection,
    is_users_route,
    update_route_car_in_collection
)
from services.statistics_app.mongo_db_utils.transport_app.train_helpers import (
    save_route_train_in_collection,
    update_route_train_in_collection,
)
from services.statistics_app.mongo_db_utils.transport_app.user_helpers import (
    is_user_exists_in_mongodb,
    save_user_in_collection
)


def store_route_cars_in_collection(route_data):
    '''
    Saving or updating db_response in mongo_db collection
    '''
    ROUTE_TYPE = 'cars_data'
    #
    if not is_user_exists_in_mongodb(route_data.get('user_data')):
        save_user_in_collection(user_data=route_data.get('user_data'))
        #
        save_route_car_in_collection(route_data=route_data)
        return 'new route cars created'
    else:
        if not is_users_route(route_data=route_data, route_type=ROUTE_TYPE):
            save_route_car_in_collection(route_data=route_data)
            return 'new route cars created'
        else:
            update_route_car_in_collection(route_data=route_data)
            return 'route and car updated'


def store_route_trains_in_collection(route_data):
    '''
    Saving or updating db_response in mongo_db collection
    '''
    ROUTE_TYPE = 'trains_data'
    #
    if not is_user_exists_in_mongodb(route_data.get('user_data')):
        save_user_in_collection(user_data=route_data.get('user_data'))
        #
        save_route_train_in_collection(route_data=route_data)
        return 'new route trains created'
    else:
        if not is_users_route(route_data=route_data, route_type=ROUTE_TYPE):
            save_route_train_in_collection(route_data=route_data)
            return 'new route cars created'
        else:
            update_route_train_in_collection(route_data=route_data)
            return 'route and train updated'
