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
    update_api_response_in_route_and_car_models
)


def get_route_data(payload):
    '''
    Return Route data
    '''
    route = is_route_exists(payload)
    if route:
        route_parsed_1_hour_ago = is_route_parsed_1_hour_ago(payload)
        if not route_parsed_1_hour_ago:
            #
            db_cars_data = get_cars_db_data(payload)
            db_trains_data = get_trains_db_data(payload)
            #
            result = {
                'cars_data': db_cars_data,
                'trains_data': db_trains_data,
            }
        #
            return result
        elif route_parsed_1_hour_ago:
            #
            api_cars_data = get_cars_api_data(payload)
            # api_trains_data = get_trains_api_data(payload)
            #
            # save_api_response_in_route_and_car_models(api_cars_data)
            update_api_response_in_route_and_car_models(api_cars_data)
            result = {
                'cars_data': api_cars_data,
                # 'trains_data': api_trains_data,
            }
            return result
    elif not route:
        #
        api_cars_data = get_cars_api_data(payload)
        # api_trains_data = get_trains_api_data(payload)
        #
        # save_api_response_in_route_and_train_models(api_cars_data)
        save_api_response_in_route_and_car_models(api_cars_data)
        #
        result = {
            'cars_data': api_cars_data,
            # 'trains_data': api_trains_data,
        }
        return result
