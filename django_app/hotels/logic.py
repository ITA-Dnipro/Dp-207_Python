import json
from datetime import timedelta, datetime
import os
from .models import City, Hotel
import requests
import jwt


# create jwt token
def create_jwt_token(city):
    hotels_app_jwt_secret = os.environ.get('HOTELS_APP_JWT_SECRET_KEY')
    payload = {
        "exp": datetime.utcnow() + timedelta(hours=24),
        "city_name": city,
    }
    token = jwt.encode(payload, hotels_app_jwt_secret, algorithm="HS256")
    return {'Authorization': token}


# create class which manage api response and creates objects for city and hotel
class CityHotels:

    def __init__(self, city):
        self.city = city
        self.url = os.environ.get('HOTELS_API_GET_ALL_HOTELS')

    # get data from api response
    def get_data_from_api(self):
        headers = create_jwt_token(self.city)
        query = {"city": self.city}
        res = requests.post(self.url, json=query, headers=headers)
        data_js = res.json()
        data = json.loads(json.dumps(data_js))
        return data

    # create city and hotels by data info
    def create_city_and_hotels(self):
        city = City.objects.filter(name=self.city).first()


        if not city:
            try:
                data = self.get_data_from_api()
                print(data)
            except Exception:
                return False
            city = City(name=self.city)
            city.save()

            for obj in data:
                hotel_ = Hotel.objects.filter(name=obj['hotel_name']).first()
                if not hotel_:
                    new_hotel = Hotel(name=obj['hotel_name'],
                                      adress=obj['adress'],
                                      price=obj['prices'],
                                      details=obj['detail'],
                                      url=obj['photo'],
                                      contacts=obj['contacts'],
                                      city=city)
                    new_hotel.save()
        return True
