from services.statistics_app.mongo_db_utils.transport_app.user_helpers import (
    get_user_from_collection,
)
from statistics_app.tests_data.user_data import test_user_data


def test_get_user_from_mongodb(add_user_in_mongodb):
    '''
    Test for adding user in mongodb collection
    '''
    user = get_user_from_collection(user_data=test_user_data)
    #
    assert user.username == test_user_data.get('username')
