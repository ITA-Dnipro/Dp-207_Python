import pytest
from transport.models import Car, Route, Train


@pytest.mark.django_db
def test_empty_route_table(db):
    routes = Route.objects.exists()
    assert routes is False


@pytest.mark.django_db
def test_empty_car_table(db):
    cars = Car.objects.exists()
    assert cars is False


@pytest.mark.django_db
def test_empty_train_table(db):
    trains = Train.objects.exists()
    assert trains is False


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_route_table_with_added_route(add_car_data_to_db):
    route = Route.objects.get(id=1)
    assert route.departure_name == 'Полтава'
    assert route.source_name == 'poezdato/blablacar'


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_car_table_with_added_car(add_car_data_to_db):
    car = Car.objects.get(id=1)
    assert car.departure_name == 'Полтава'


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_train_table_with_added_train(add_train_data_to_db):
    train = Train.objects.get(id=1)
    assert train.departure_name == 'Киев'
