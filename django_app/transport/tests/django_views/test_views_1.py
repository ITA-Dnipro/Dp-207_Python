from lxml import html
import pytest
from transport.tests_data.car_data import (
    car_route_departure_date,
    car_route_departure_date_response_format,
    car_departure_date_in_future_response_format,
)
from transport.tests_data.train_data import (
    train_route_departure_date,
    train_route_departure_date_response_format,
    train_departure_date_in_future_response_format
)


def test_get_transport_main_view(client):
    '''
    Test GET /transport/
    '''
    response = client.get('/transport/')
    tree = html.fromstring(response.content)
    h3_welcome_msg = tree.xpath(
        '//*/div/h3/text()'
    )
    assert 'Welcome to the Transport search' == h3_welcome_msg[0]


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_post_transport_route_view_car_data(client, add_car_data_to_db):
    '''
    Test POST /transport/schedule/ with valid form data and route + car
    added to the tables
    '''
    form_data = {
        'departure_name': 'Полтава',
        'departure_date': f'{car_route_departure_date}',
        'arrival_name': 'Николаев',
        'transport_types': ['car']
    }
    #
    response = client.post(
        '/transport/schedule',
        data=form_data,
        follow=True
    )
    #
    tree = html.fromstring(response.content)
    #
    route_departure_arrival_name = tree.xpath(
        '//*/div[@id="route_section"]/a/h4/text()'
    )
    #
    route_departure_data = tree.xpath(
        '//*/div[@id="route_section"]/h5/text()'
    )
    #
    car_departure_arrival_name = tree.xpath(
        '//*/div[@id="trips_section"]/table/tbody/tr[1]/th[3]/text()'
    )
    car_departure_date = tree.xpath(
        '//*/div[@id="trips_section"]/table/tbody/tr[1]/th[4]/text()'
    )
    # route
    assert 'Полтава - Николаев' == route_departure_arrival_name[0]
    assert (
        f'{car_route_departure_date_response_format}'
        '\n    \n\n' == route_departure_data[0]
    )
    # car
    assert 'Полтава - Николаев' == car_departure_arrival_name[0]
    assert f'{car_departure_date_in_future_response_format}' \
        == car_departure_date[0]


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_post_transport_route_view_train_data(client, add_train_data_to_db):
    '''
    Test POST /transport/schedule/ with valid form data and route + train
    added to the tables
    '''
    form_data = {
        'departure_name': 'Киев',
        'departure_date': f'{train_route_departure_date}',
        'arrival_name': 'Одесса',
        'transport_types': ['train']
    }
    #
    response = client.post(
        '/transport/schedule',
        data=form_data,
        follow=True
    )
    #
    tree = html.fromstring(response.content)
    #
    route_departure_arrival_name = tree.xpath(
        '//*/div[@id="route_section"]/h4/text()'
    )
    # #
    route_departure_data = tree.xpath(
        '//*/div[@id="route_section"]/h5/text()'
    )
    # #
    train_departure_arrival_name = tree.xpath(
        '//*/div[@id="trips_section"]/table/tbody/tr[1]/th[3]/text()'
    )
    train_departure_date = tree.xpath(
        '//*/div[@id="trips_section"]/table/tbody/tr[1]/th[4]/text()'
    )
    # route
    assert 'Киев - Одесса' == route_departure_arrival_name[0]
    assert f'{train_route_departure_date_response_format}' == \
        route_departure_data[0]
    # # train
    assert 'Киев - Одесса' == train_departure_arrival_name[0]
    assert f'{train_departure_date_in_future_response_format}' == \
        train_departure_date[0]
