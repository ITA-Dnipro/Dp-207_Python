from services.statistics_app.mongo_db_utils.transport_app.route_helpers import (
    add_hash_to_db_response,
    is_route_exist_in_mongodb,
    save_route_car_in_collection,
    save_route_train_in_collection,
    is_route_hash_differs,
    update_route_car_in_collection,
    update_route_train_in_collection,
)


def store_route_cars_in_collection(route_data):
    '''
    Saving or updating db_response in mongo_db collection
    '''
    db_response = route_data.get('cars_data')
    db_response = add_hash_to_db_response(db_response=db_response)
    route_exists = is_route_exist_in_mongodb(db_response=db_response)
    #
    if not route_exists:
        save_route_car_in_collection(route_data=route_data)
        return 'new route created'
    else:
        found_by_hash = is_route_hash_differs(db_response=db_response)
        if found_by_hash:
            return 'same route doing nothing'
        else:
            update_route_car_in_collection(db_response=db_response)
            return 'route and car updated'


def store_route_trains_in_collection(route_data):
    '''
    Saving or updating db_response in mongo_db collection
    '''
    db_response = route_data.get('trains_data')
    db_response = add_hash_to_db_response(db_response=db_response)
    #
    route_exists = is_route_exist_in_mongodb(db_response=db_response)
    #
    if not route_exists:
        save_route_train_in_collection(route_data=route_data)
        return 'new route created'
    else:
        found_by_hash = is_route_hash_differs(db_response=db_response)
        if found_by_hash:
            return 'same route doing nothing'
        else:
            update_route_train_in_collection(db_response=db_response)
            return 'route and train updated'
