import pytest
from statistics_app.tests_data.user_data import test_user_data
from services.statistics_app.mongo_db_utils.transport_app.user_helpers import (
    save_user_in_collection,
    delete_user_from_collection
)


@pytest.fixture(scope='function')
def add_user_in_mongodb():
    '''
    Add user to mongodb fixture
    '''
    delete_user_from_collection(user_data=test_user_data)
    #
    yield save_user_in_collection(user_data=test_user_data)
    #
    delete_user_from_collection(user_data=test_user_data)
