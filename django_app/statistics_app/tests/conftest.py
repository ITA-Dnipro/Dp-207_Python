import pytest
from statistics_app.tests_data.user_data import test_user_data
from statistics_app.tests_data.route_car_data import route_cars_data
from services.statistics_app.mongo_db_utils.transport_app.user_helpers import (
    save_user_in_collection,
    delete_user_from_collection
)
from services.statistics_app.celery_utils.celery_tasks.transport_app.transport_tasks_1 import (
    save_transport_data_to_mongo_db
)
from services.statistics_app.mongo_db_utils.transport_app.route_crud import (
    delete_delete_user_route_cars_data
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


@pytest.fixture(scope='function')
def add_user_route_car_in_mongodb():
    '''
    Add user, route, car data to mongodb
    '''
    delete_delete_user_route_cars_data(
        route_data=route_cars_data,
        user_data=test_user_data
    )
    yield save_transport_data_to_mongo_db(
        route_data=route_cars_data,
        user_data=test_user_data,
    )
    delete_delete_user_route_cars_data(
        route_data=route_cars_data,
        user_data=test_user_data
    )
