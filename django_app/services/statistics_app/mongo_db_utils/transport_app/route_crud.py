from services.statistics_app.mongo_db_utils.transport_app.route_helpers import (
    add_hash_to_db_response,
    is_route_exist_in_mongodb,
    save_route_car_in_collection,
    save_route_train_in_collection
)


def store_route_cars_in_collection(db_response):
    '''
    Saving or updating db_response in mongo_db collection
    '''
    db_response = add_hash_to_db_response(db_response=db_response)
    route_exists = is_route_exist_in_mongodb(db_response=db_response)
    #
    if not route_exists:
        save_route_car_in_collection(db_response=db_response)
        return 'new route created'


def store_route_trains_in_collection(db_response):
    '''
    Saving or updating db_response in mongo_db collection
    '''
    db_response = add_hash_to_db_response(db_response=db_response)
    #
    route_exists = is_route_exist_in_mongodb(db_response=db_response)
    #
    if not route_exists:
        save_route_train_in_collection(db_response=db_response)
        return 'new route created'
