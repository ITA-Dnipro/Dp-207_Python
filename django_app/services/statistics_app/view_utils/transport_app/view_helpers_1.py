from services.statistics_app.mongo_db_utils.mongo_db_client import transport_client, user_client # noqa
from services.statistics_app.mongo_db_utils.transport_app.mongo_models import (
    User, Route, Car, Train
)


def get_last_20_users():
    '''
    Return last 20 users from mongodb
    '''
    users = User.objects[:20]
    return users
