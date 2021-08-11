from services.statistics_app.mongo_db_utils.mongo_db_client import transport_client, user_client # noqa
from services.statistics_app.mongo_db_utils.transport_app.mongo_models import (
    Route
)
from services.statistics_app.mongo_db_utils.transport_app.user_helpers import (
    get_user_from_collection
)
from mongoengine.errors import DoesNotExist


def get_route_from_collection(route_data, route_type):
    '''
    Return Route object
    '''
    db_response = route_data.get(route_type)
    user = get_user_from_collection(user_data=route_data.get('user_data'))
    try:
        route = Route.objects(
            user=user,
            departure_name=db_response.get('departure_name'),
            departure_date=db_response.get('departure_date'),
            arrival_name=db_response.get('arrival_name'),
            source_name=db_response.get('source_name'),
        ).get()
        #
        return route
    except DoesNotExist:
        return False
