import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from .api_utils.api_request_helpers import create_api_call
import json
from .models import Route, Car, Train

load_dotenv()


def create_jwt_token(payload):
    '''
    Return JWT token encoded with .env file sekret
    '''
    TRANSPORT_APP_JWT_SECRET = os.environ.get('TRANSPORT_APP_JWT_SECRET')
    #
    incoming_date = dict(payload)
    incoming_date['exp'] = datetime.utcnow() + timedelta(seconds=300)
    #
    token = jwt.encode(
        incoming_date,
        TRANSPORT_APP_JWT_SECRET,
        algorithm="HS256"
    )
    return token


class Transport:

    def __init__(self, departure_place, arrival_place, departure_date):
        self.departure_place = departure_place.capitalize()
        self.arrival_place = arrival_place.capitalize()
        self.departure_date = departure_date
        self.url = os.environ.get('TRANSPORT_APP_API_CARS_URL')

    def change_time_format(self, date):
        format1 = '%Y-%m-%d'
        format2 = '%d.%m.%Y'
        date_formatted = datetime.strptime(date, format1).strftime(format2)
        return date_formatted

    def get_api_transport_details(self):
        payload = {
            "departure_name": self.departure_place,
            "departure_date": self.change_time_format(self.departure_date),
            "arrival_name": self.arrival_place,
        }
        TRANSPORT_APP_API_CARS_URL = os.environ.get('TRANSPORT_APP_API_CARS_URL')
        api_response = create_api_call(payload, TRANSPORT_APP_API_CARS_URL)
        context = json.loads(api_response.text)
        return context

    def create_route(self):
        # departure_place = Route.objects.filter(name=self.departure_place)
        # arrival_place = Route.objects.filter(name=self.arrival_place)
        # if not departure_place and arrival_place:
        parsed_data = self.get_api_transport_details()
        parsed_time = datetime.strptime(parsed_data.get("parsed_time"),
                                        '%d-%m-%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

        new_route = Route.objects.create(
            departure_name=self.departure_place,
            arrival_name=self.arrival_place,
            departure_date=self.departure_date,
            parsed_time=parsed_time,
            source_name=parsed_data.get("source_name"),
            source_url=parsed_data.get("source_url"),
        )
        new_route.save()
        return True
