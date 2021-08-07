import scrapy
from scrapy.http import JsonRequest
import json
from datetime import datetime
import pytz
from ..middlewares import RandomUserAgentMiddleware


class PoezdUaSpider(scrapy.Spider):
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            (
                'scrapy.contrib.downloadermiddleware.'
                'useragent.UserAgentMiddleware'
                ): None,
            (
                RandomUserAgentMiddleware
            ): 400
        },
        'HTTPERROR_ALLOWED_CODES': [418, 411],
    }

    name = 'poezd_ua'
    start_urls = ['http://poezd.ua/']

    def __init__(self, *args, **kwargs):
        self.departure_name = kwargs['departure_name'].lower().capitalize()
        self.departure_date = kwargs['departure_date']
        self.arrival_name = kwargs['arrival_name'].lower().capitalize()
        #
        self.POEZD_POST_URL = 'https://poezd.ua/zd'

    def parse(self, response):
        json_payload = {
            "action": "search",
            "from": self.departure_name,
            "to": self.arrival_name,
            "date": self.departure_date,
            "return_date": "",
            "schedule": False
        }
        yield JsonRequest(
            url=self.POEZD_POST_URL,
            data=json_payload,
            callback=self.api_response_handler,
            method="POST"
        )

    def api_response_handler(self, response):
        result_dict = {}
        if response.status == 418:
            result_dict['result'] = False
            result_dict['error_code'] = response.status
        elif response.status == 411:
            result_dict['result'] = False
            result_dict['error_code'] = response.status
        else:
            jsonresponse = json.loads(response.text)
            #
            kyiv_tz = pytz.timezone('Europe/Kiev')
            parsed_time = datetime.now(tz=kyiv_tz).strftime(
                "%d-%m-%Y %H:%M:%S"
            )
            #
            result_dict['result'] = True
            result_dict['departure_name'] = self.departure_name
            result_dict['departure_date'] = self.departure_date
            result_dict['arrival_name'] = self.arrival_name
            result_dict['parsed_time'] = parsed_time
            result_dict['source_name'] = 'poezd.ua'
            result_dict['source_url'] = response.url
            result_dict['trips'] = []
            for station_type in jsonresponse['departure']:
                if station_type['type'] == 'main':
                    for train in station_type['train']:
                        #
                        result_train_dict = {}
                        #
                        result_train_dict['train_name'] = train.get('name')
                        result_train_dict['train_number'] = train.get('number')
                        result_train_dict['train_uid'] = (
                            station_type.get(
                                'trains_uids'
                            ).get(
                                train.get('number')
                            )
                        )
                        result_train_dict['departure_name'] = (
                            train.get('station_from', {}).get('name')
                        )
                        result_train_dict['departure_code'] = (
                            train.get('station_from', {}).get('code')
                        )
                        result_train_dict['departure_date'] = (
                            train.get('departure_date', {}).get('original')
                        )
                        result_train_dict['arrival_name'] = (
                            train.get('station_to', {}).get('name')
                        )
                        result_train_dict['arrival_code'] = (
                            train.get('station_to', {}).get('code')
                        )
                        result_train_dict['arrival_date'] = (
                            train.get('arrival_date', {}).get('original')
                        )
                        result_train_dict['in_route_time'] = (
                            train.get('travel_time', {}).get('human')
                        )
                        result_train_dict['parsed_time'] = parsed_time
                        result_train_dict['source_name'] = 'poezd.ua'
                        result_train_dict['source_url'] = response.url
                        #
                        result_dict['trips'].append(result_train_dict)
        #
        yield result_dict
