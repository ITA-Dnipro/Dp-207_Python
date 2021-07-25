import requests
from requests.exceptions import ConnectionError
import os
from .jwt_helpers import create_jwt_token
from dotenv import load_dotenv
import json
from services.transport_app.models_utils.models_helpers import (
    save_api_response_in_route_and_train_models,
    save_api_response_in_route_and_car_models
)
from .api_response_helpers import (
    car_api_response_time_converter,
    train_api_response_time_converter
)
load_dotenv()


def create_api_call(payload, api_endpoint):
    '''
    Return requests Response object
    '''
    TRANSPORT_APP_SERVICE_NAME = os.environ.get('TRANSPORT_APP_SERVICE_NAME')
    TRANSPORT_APP_SERVICE_PORT = os.environ.get('TRANSPORT_APP_SERVICE_PORT')
    TRANSPORT_API_URL = (
        f'http://{TRANSPORT_APP_SERVICE_NAME}:{TRANSPORT_APP_SERVICE_PORT}/'
        f'{api_endpoint}'
    )
    jwt_token = create_jwt_token(payload)
    headers = {'authorization': jwt_token}
    try:
        api_response = requests.post(
            url=TRANSPORT_API_URL,
            headers=headers,
            json=payload
        )
        return api_response
    except ConnectionError as e:
        return {'error': e.args[0].args[0]}


def get_trains_api_data(payload):
    '''
    Return response from trains API
    '''
    TRANSPORT_APP_API_TRAINS_URL = os.environ.get(
        'TRANSPORT_APP_API_TRAINS_URL'
    )
    api_response = create_api_call(payload, TRANSPORT_APP_API_TRAINS_URL)
    api_response = json.loads(api_response.text)
    #
    if api_response['result'] is False:
        return api_response
    #
    save_api_response_in_route_and_train_models(api_response)
    #
    api_response = train_api_response_time_converter(api_response)
    return api_response


def get_cars_api_data(payload):
    '''
    Return response from cars API
    '''
    TRANSPORT_APP_API_CARS_URL = os.environ.get('TRANSPORT_APP_API_CARS_URL')
    api_response = create_api_call(payload, TRANSPORT_APP_API_CARS_URL)
    api_response = json.loads(api_response.text)
    #
    if api_response['result'] is False:
        return api_response
    #
    save_api_response_in_route_and_car_models(api_response)
    #
    api_response = car_api_response_time_converter(api_response)
    return api_response
