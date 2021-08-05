from .jwt_token import create_jwt_token
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


# get data for hotels by city from flask service
def get_data_for_hotels_by_city(city):
    url = os.environ.get('HOTELS_API_GET_ALL_HOTELS')
    headers = create_jwt_token(city)
    query = {"city": city}
    res = requests.post(url, json=query, headers=headers)
    if res.status_code == 200:
        data_js = res.json()
        data = json.loads(json.dumps(data_js))
        return data
    elif res.status_code == 404:
        raise CityNotExists('Такого города не найдено')
    elif res.status_code == 500 and res.json().get('msg'):
        raise SomeProblemWithParsing('Попробуйте еще раз!')


# get data for hotel rooms from api
def get_for_hotel_rooms(city, hotel_href, date_of_departure, date_of_arrival):
    url = os.environ.get('HOTELS_API_GET_ROOMS_FOR_HOTEL')
    headers = create_jwt_token(city)
    query = {
        "hotel_href": hotel_href,
        "date_of_departure": date_of_departure,
        "date_of_arrival": date_of_arrival
             }
    res = requests.post(url, json=query, headers=headers)
    if res.status_code == 200:
        data_js = res.json()
        data = json.loads(json.dumps(data_js))
        return data
    elif res.status_code == 500 and res.json().get('msg'):
        raise SomeProblemWithParsing('Попробуйте еще раз!')


def send_msg(text):
    URL = os.environ.get('TELEGRAM_BOT_SEND_MSG')
    chat_id = 894349543
    answer = {'chat_id': chat_id, 'text': text}
    requests.post(URL, json=answer)
