def update_route_car_document(route, route_filter, db_response):
    '''
    Update route and car document in collection
    '''
    route_update_dict = {
        'departure_name': db_response.get('departure_name'),
        'arrival_name': db_response.get('arrival_name'),
        'departure_date': db_response.get('departure_date'),
        'parsed_time': db_response.get('parsed_time'),
        'source_name': db_response.get('source_name'),
        'source_url': db_response.get('source_url'),
        'result': db_response.get('result'),
        'route_hash': db_response.get('route_hash'),
        'mongo_updated': db_response.get('mongo_updated'),
    }
    #
    cars = db_response.get('trips')
    #
    route.update_one(
        filter=route_filter,
        update={
                '$set': route_update_dict,
                '$addToSet': {'trips': {'$each': cars}}
            },
        upsert=True,
    )


def remove_fields_from_db_response(db_response):
    '''
    Removes extra fields from db_response, and return db_response
    '''
    db_response.pop('id')
    #
    cars = db_response.get('trips')
    [car.pop('id') for car in cars]
    [car.pop('route_id_id') for car in cars]
    [car.pop('parsed_time') for car in cars]
    #
    return db_response
