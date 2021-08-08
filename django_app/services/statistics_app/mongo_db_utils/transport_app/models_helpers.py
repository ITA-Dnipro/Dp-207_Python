from services.statistics_app.mongo_db_utils.transport_app.route_helpers import (
    get_route_collection,
    add_hash_to_db_response,
    is_route_exist_in_mongodb,
    is_route_hash_differs
)
from services.statistics_app.mongo_db_utils.transport_app.car_helpers import (
    remove_fields_from_db_response,
    update_route_car_document
)


def store_route_cars_in_collection(db_response):
    '''
    Saving or updating db_response in mongo_db collection
    '''
    route = get_route_collection()
    #
    db_response = add_hash_to_db_response(db_response=db_response)
    #
    db_response = remove_fields_from_db_response(db_response=db_response)
    #
    route_filter = {
        'departure_name': db_response.get('departure_name'),
        'departure_date': db_response.get('departure_date'),
        'arrival_name': db_response.get('arrival_name'),
        'source_name': db_response.get('source_name'),
    }
    route_exists = is_route_exist_in_mongodb(route=route, route_filter=route_filter)
    #
    if not route_exists:
        route.insert_one(db_response)
        return 'new route created'
    else:
        hash_filter = {
            'route_hash': db_response.get('route_hash'),
        }
        #
        found_by_hash = is_route_hash_differs(route=route, hash_filter=hash_filter)
        if found_by_hash:
            return 'same route doing nothing'
        else:
            update_route_car_document(
                route=route,
                route_filter=route_filter,
                db_response=db_response
            )
            return 'route updated'
