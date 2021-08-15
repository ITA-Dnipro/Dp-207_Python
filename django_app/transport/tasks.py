from celery import shared_task
from services.transport_app.view_utils.view_helpers import get_route_data


# task for fetch data from api
@shared_task()
def get_routes(payload):
    data = get_route_data(payload)
    return data
