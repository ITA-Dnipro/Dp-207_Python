from hotels.utils.jwt_token import create_jwt_token
import requests
import json
import os


class CustomException(Exception):
    def __init__(self, msg):
        self.msg = msg


class CityNotExists(CustomException):
    pass


class SomeProblemWithParsing(CustomException):
    pass


# get data for city from flask service
def get_city(city):
    url = os.environ.get('HOTELS_API_GET_CITY')
    headers = create_jwt_token(city)
    query = {"city": city}
    res = requests.post(url, json=query, headers=headers)
    if res.status_code == 200:
        data_js = res.json()
        data = json.loads(json.dumps(data_js))
        return data
    elif res.status_code == 404:
        raise CityNotExists(f'Такого города как "{city}" не найдено')
    elif res.status_code == 500 and res.json().get('msg'):
        raise SomeProblemWithParsing('Попробуйте еще раз!')

