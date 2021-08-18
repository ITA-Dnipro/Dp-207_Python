import pytest
import copy
from services.transport_app.models_utils.car_helpers import (
    save_api_response_in_route_and_car_models
)
from transport.tests_data.car_data import route_car
from services.transport_app.models_utils.train_helpers import (
    save_api_response_in_route_and_train_models
)
from transport.tests_data.train_data import route_train


@pytest.fixture(scope='function')
def add_car_data_to_db(django_db_blocker):
    '''
    Fixture that populates tests database's route and car tables
    with route and car data
    '''
    with django_db_blocker.unblock():
        test_route_car = copy.deepcopy(route_car)
        yield save_api_response_in_route_and_car_models(test_route_car)


@pytest.fixture(scope='function')
def add_train_data_to_db(django_db_blocker):
    '''
    Fixture that populates tests database's route and train tables
    with route and train data
    '''
    with django_db_blocker.unblock():
        test_route_train = copy.deepcopy(route_train)
        yield save_api_response_in_route_and_train_models(test_route_train)
