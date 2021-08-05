from services.statistics_app.celery_utils.celery_app import app


@app.task
def save_cars_db_data_to_mongo_db(db_response):
    return 'saving cars db data to mongodb'
