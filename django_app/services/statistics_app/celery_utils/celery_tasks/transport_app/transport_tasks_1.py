from services.statistics_app.celery_utils.celery_app import app
from services.statistics_app.mongo_db_utils.transport_app.route_crud import (
    store_route_cars_in_collection,
    store_route_trains_in_collection
)


@app.task
def save_cars_db_data_to_mongo_db(db_response):
    result = store_route_cars_in_collection(db_response=db_response)
    return result


@app.task
def save_trains_db_data_to_mongo_db(db_response):
    '''
    Celery task that calls function that stores route and train data
    in mongodb collection
    '''
    result = store_route_trains_in_collection(db_response=db_response)
    return result
