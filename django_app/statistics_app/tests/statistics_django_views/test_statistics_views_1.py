from lxml import html
from statistics_app.tests_data.user_data import test_user_data
from statistics_app.tests_data.route_car_data import (
    search_route_car_data
)


def test_get_statistics_home_page(admin_client):
    '''
    Test admin user GET '/statistics/' page
    '''
    response = admin_client.get('/statistics/')
    #
    tree = html.fromstring(response.content)
    transport_h5_msg = tree.xpath(
        '//*/div[@class="card-body"]/h5/text()'
    )
    assert 'Transport' == transport_h5_msg[0]


def test_get_statistics_transport_home_page(admin_client):
    '''
    Test admin user GET '/statistics/transport/' page
    '''
    response = admin_client.get('/statistics/transport')
    #
    tree = html.fromstring(response.content)
    transport_welcome_msg = tree.xpath(
        '//*/div[@id="transport_section"]/h4/text()'
    )
    #
    assert 'Welcome to Transport statistics' == transport_welcome_msg[0]


def test_post_statistics_user_page_with_no_user_added(admin_client):
    '''
    Test admin user POST '/statistics/user_page_form_handler' page
    with user not added to mongodb
    '''
    form_data = {
        'username': test_user_data.get('username'),
    }
    response = admin_client.post(
        '/statistics/user_page_form_handler',
        data=form_data,
        follow=True,
    )
    #
    tree = html.fromstring(response.content)
    user_not_found_msg = tree.xpath(
        '//*/div[@id="user_not_found"]/h3/text()'
    )
    #
    assert 'User does not exists.' == user_not_found_msg[0]


def test_post_statistics_user_page_with_user_added(admin_client, add_user_in_mongodb):
    '''
    Test admin user GET '/statistics/transport/' page
    with test user added to mongodb
    '''
    form_data = {
        'username': test_user_data.get('username'),
    }
    response = admin_client.post(
        '/statistics/user_page_form_handler',
        data=form_data,
        follow=True,
    )
    #
    tree = html.fromstring(response.content)
    user_not_found_msg = tree.xpath(
        '//*/div[@id="users_section"]/h3/text()'
    )
    #
    assert f'Search {test_user_data.get("username")} routes' == user_not_found_msg[0]


def test_post_statistics_user_page_with_route_data_added(
        admin_client, add_user_route_car_in_mongodb
        ):
    '''
    Test admin user GET '/statistics/transport/' page
    with test user added to mongodb
    '''
    form_data = {
        'departure_name': search_route_car_data.get('departure_name'),
        'departure_date': search_route_car_data.get('departure_date'),
        'arrival_name': search_route_car_data.get('arrival_name'),
        'transport_types': search_route_car_data.get('transport_types'),
    }
    username = test_user_data.get('username')
    #
    response = admin_client.post(
        f'/statistics/route_page_form_handler/{username}',
        data=form_data,
        follow=True,
    )
    #
    tree = html.fromstring(response.content)
    user_routes_msg = tree.xpath(
        '//*/div[@id="users_section"]/h4/text()'
    )
    route_from_to = tree.xpath(
        '//*/div[@id="users_section"]/table/tbody/tr/th[2]/text()'
    )
    #
    assert f'{test_user_data.get("username")} route statistics' == user_routes_msg[0]
    assert 'Днепр - Запорожье' == route_from_to[0]
