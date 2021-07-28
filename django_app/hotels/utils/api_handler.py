from .jwt_token import create_jwt_token
import requests
import json
import os


# get data for hotels by city from flask service
def get_data_for_hotels_by_city(city):
    url = os.environ.get('HOTELS_API_GET_ALL_HOTELS')
    headers = create_jwt_token(city)
    query = {"city": city}
    res = requests.post(url, json=query, headers=headers)
    data_js = res.json()
    data = json.loads(json.dumps(data_js))
    return data


# get data for hotel rooms from api
def get_for_hotel_rooms(city, hotel, date_of_departure, date_of_arrival):
    url = os.environ.get('HOTELS_API_GET_ROOMS_FOR_HOTEL')
    headers = create_jwt_token(city)
    query = {
        "hotel": hotel,
        "date_of_departure": date_of_departure,
        "date_of_arrival": date_of_arrival
             }
    res = requests.post(url, json=query, headers=headers)
    try:
        data_js = res.json()
        data = json.loads(json.dumps(data_js))
        return data
    except Exception:
        data = {'msg': 'error'}
        return data

