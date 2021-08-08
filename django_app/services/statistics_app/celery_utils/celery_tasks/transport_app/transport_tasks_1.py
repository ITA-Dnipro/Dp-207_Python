from services.statistics_app.celery_utils.celery_app import app
from services.statistics_app.mongo_db_utils.transport_app.models_helpers import (
    store_route_cars_in_collection
)


@app.task
def save_cars_db_data_to_mongo_db(db_response):
    result = store_route_cars_in_collection(db_response=db_response)
    return result
