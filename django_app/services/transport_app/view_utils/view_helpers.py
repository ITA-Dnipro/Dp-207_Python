from services.transport_app.models_utils.models_helpers import (
    get_cars_db_data, get_trains_db_data, is_route_exists,
    is_route_parsed_1_hour_ago
)
from services.transport_app.api_utils.api_request_helpers import (
    get_cars_api_data, get_trains_api_data
)
from services.transport_app.models_utils.models_helpers import (
    save_api_response_in_route_and_train_models,
    save_api_response_in_route_and_car_models,
    update_api_response_in_route_and_car_models,
    update_api_response_in_route_and_train_models
)


CARS_SOURCE_NAME = 'poezdato/blablacar'
TRAINS_SOURCE_NAME = 'poezd.ua'


def get_route_data(payload):
    '''
    Return Route data
    '''
    transport_types_funcs = {
        'car': get_cars_data,
        'train': get_trains_data
    }
    result = {}
    for tr in payload['transport_types']:
        #
        data = transport_types_funcs[tr](payload)
        #
        for key, value in data.items():
            result[key] = value
    #
    return result


def get_cars_data(payload):
    '''
    Return cars data
    '''
    route = is_route_exists(payload, CARS_SOURCE_NAME)
    if route:
        route_parsed_1_hour_ago = is_route_parsed_1_hour_ago(
            payload,
            CARS_SOURCE_NAME
        )
        if not route_parsed_1_hour_ago:
            #
            db_cars_data = get_cars_db_data(
                payload,
                CARS_SOURCE_NAME
            )
            #
            result = {
                'cars_data': db_cars_data,
            }
            return result
        elif route_parsed_1_hour_ago:
            #
            api_cars_data = get_cars_api_data(payload)
            #
            if api_cars_data.get('result') is False:
                return {'cars_data': api_cars_data}
            #
            update_api_response_in_route_and_car_models(api_cars_data)
            #
            result = {
                'cars_data': api_cars_data,
            }
            return result
    elif not route:
        #
        api_cars_data = get_cars_api_data(payload)
        if api_cars_data.get('result') is False:
            return {'cars_data': api_cars_data}
        #
        save_api_response_in_route_and_car_models(api_cars_data)
        #
        result = {
            'cars_data': api_cars_data,
        }
        return result


def get_trains_data(payload):
    '''
    Return trains data
    '''
    route = is_route_exists(payload, TRAINS_SOURCE_NAME)
    if route:
        route_parsed_1_hour_ago = is_route_parsed_1_hour_ago(
            payload,
            TRAINS_SOURCE_NAME
        )
        if not route_parsed_1_hour_ago:
            #
            db_trains_data = get_trains_db_data(
                payload,
                TRAINS_SOURCE_NAME
            )
            #
            result = {
                'trains_data': db_trains_data,
            }
            #
            return result
        elif route_parsed_1_hour_ago:
            #
            api_trains_data = get_trains_api_data(payload)
            #
            if api_trains_data.get('result') is False:
                return {'trains_data': api_trains_data}
            #
            update_api_response_in_route_and_train_models(api_trains_data)
            #
            result = {
                'trains_data': api_trains_data,
            }
            return result
    elif not route:
        #
        api_trains_data = get_trains_api_data(payload)
        #
        if api_trains_data.get('result') is False:
            return {'trains_data': api_trains_data}
        #
        save_api_response_in_route_and_train_models(api_trains_data)
        #
        result = {
            'trains_data': api_trains_data,
        }
        return result
