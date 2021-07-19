import requests
from requests.exceptions import ConnectionError
import os
from .jwt_helpers import create_jwt_token
from dotenv import load_dotenv

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
