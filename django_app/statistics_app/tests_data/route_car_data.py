import datetime
import pytz

route_cars_data = {
    'cars_data': {
        'id': 17,
        'departure_name': 'Днепр',
        'arrival_name': 'Запорожье',
        'departure_date': datetime.datetime(2021, 8, 16, 21, 0, tzinfo=pytz.utc),
        'parsed_time': datetime.datetime(2021, 8, 15, 15, 47, 43, tzinfo=pytz.utc),
        'source_name': 'poezdato/blablacar',
        'source_url': 'https://www.blablacar.com.ua/search?fc=48.477883,35.014131&tc=47.795198,35.187524&fn=Дніпро&tn=Запоріжжя&db=2021-08-17&de=2021-08-17&utm_source=POEZDATO&utm_medium=API&utm_campaign=UA_POEZDATO_PSGR_OFFER_NOTRAINS&comuto_cmkt=UA_POEZDATO_PSGR_OFFER_NOTRAINS&utm_content=%D0%94%D0%BD%D0%B5%D0%BF%D1%80-%D0%97%D0%B0%D0%BF%D0%BE%D1%80%D0%BE%D0%B6%D1%8C%D0%B5', # noqa
        'trips': [
            {
                'id': 138,
                'route_id_id': 17,
                'departure_name': 'Днепр',
                'departure_date': datetime.datetime(2021, 8, 16, 23, 0, tzinfo=pytz.utc),
                'arrival_name': 'Запорожье',
                'price': '75.00 UAH',
                'car_model': 'MERCEDES 220',
                'blablacar_url': 'https://www.blablacar.com.ua/trip?source=CARPOOLING&id=2256671248-dnpro-zaporzhzhya&utm_source=POEZDATO&utm_medium=API&utm_campaign=UA_POEZDATO_PSGR_TRIPLOGIN_NOTRAINS&comuto_cmkt=UA_POEZDATO_PSGR_TRIPLOGIN_NOTRAINS&utm_content=%D0%94%D0%BD%D0%B5%D0%BF%D1%80-%D0%97%D0%B0%D0%BF%D0%BE%D1%80%D0%BE%D0%B6%D1%8C%D0%B5', # noqa
                'parsed_time': datetime.datetime(2021, 8, 15, 15, 47, 43, tzinfo=pytz.utc),
                'source_name': 'poezdato/blablacar',
                'source_url': 'https://poezdato.net/search/get-trips2?src=%D0%94%D0%BD%D0%B5%D0%BF%D1%80|48.477883,35.014131&dst=%D0%97%D0%B0%D0%BF%D0%BE%D1%80%D0%BE%D0%B6%D1%8C%D0%B5|47.795198,35.187524&date=17.08.2021&country=2&notrains=1&details=1&country_dst=2' # noqa
            }
        ],
        'result': True
    }
}
search_route_car_data = {
    'departure_name': route_cars_data['cars_data']['departure_name'],
    'arrival_name': route_cars_data['cars_data']['arrival_name'],
    'departure_date': '17.08.2021',
    'transport_types': 'car',
}
