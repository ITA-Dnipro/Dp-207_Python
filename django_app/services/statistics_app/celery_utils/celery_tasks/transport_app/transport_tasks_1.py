from services.statistics_app.celery_utils.celery_app import app
from services.statistics_app.mongo_db_utils.transport_app.route_crud import (
    store_route_cars_in_collection,
    store_route_trains_in_collection
)


@app.task
def save_transport_data_to_mongo_db(route_data, user_data):
    '''
    Celery task for saving transport data in mongodb
    '''
    if not user_data.get('username'):
        return 'anonymous user statistics not saved'
    #
    route_data['user_data'] = user_data
    #
    cars_data = route_data.get('cars_data', {}).get('result')
    trains_data = route_data.get('trains_data', {}).get('result')
    #
    if cars_data is True and trains_data is True:
        cars_result = store_route_cars_in_collection(route_data=route_data)
        trains_result = store_route_trains_in_collection(route_data=route_data)
        #
        return cars_result + trains_result
    elif cars_data is True:
        cars_result = store_route_cars_in_collection(route_data=route_data)
        return cars_result
    elif trains_data is True:
        trains_result = store_route_trains_in_collection(route_data=route_data)
        return trains_result
    else:
        return 'no route data to save'
