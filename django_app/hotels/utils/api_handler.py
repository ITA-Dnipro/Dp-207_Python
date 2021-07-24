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
