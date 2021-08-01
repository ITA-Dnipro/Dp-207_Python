from datetime import datetime, timedelta

car_route_departure_date = datetime.now().strftime("%d.%m.%Y")
car_route_departure_date_response_format = (
    datetime.now().strftime("%d-%m-%Y")
)
car_departure_date_in_future = datetime.now() + timedelta(minutes=5)
car_departure_date_in_future_response_format = (
    car_departure_date_in_future.strftime("%d-%m-%Y %H:%M:%S")
)


route_car = {
    'result': True,
    'departure_name': 'Полтава',
    'departure_date': f'{car_route_departure_date}',
    'arrival_name': 'Николаев',
    'parsed_time': f'{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}',
    'source_name': 'poezdato/blablacar',
    'source_url': 'https://www.blablacar.com.ua/search?fc=49.603405,34.524628&tc=46.958073,31.973779&fn=Полтава&tn=Миколаїв&db=2021-07-31&de=2021-07-31&utm_source=POEZDATO&utm_medium=API&utm_campaign=UA_POEZDATO_PSGR_OFFER_NOTRAINS&comuto_cmkt=UA_POEZDATO_PSGR_OFFER_NOTRAINS&utm_content=%D0%9F%D0%BE%D0%BB%D1%82%D0%B0%D0%B2%D0%B0-%D0%9D%D0%B8%D0%BA%D0%BE%D0%BB%D0%B0%D0%B5%D0%B2', # noqa
    'trips': [
        {
            'departure_name': 'Полтава',
            'departure_date': (
                f'{car_departure_date_in_future.strftime("%d/%m/%Y %H:%M:%S")}'
            ),
            'arrival_name': 'Николаев',
            'price': '575.00 UAH',
            'car_model': None,
            'blablacar_url': 'https://www.blablacar.com.ua/trip?source=CARPOOLING&id=2244950951-poltava-mikolajiv&utm_source=POEZDATO&utm_medium=API&utm_campaign=UA_POEZDATO_PSGR_TRIPLOGIN_NOTRAINS&comuto_cmkt=UA_POEZDATO_PSGR_TRIPLOGIN_NOTRAINS&utm_content=%D0%9F%D0%BE%D0%BB%D1%82%D0%B0%D0%B2%D0%B0-%D0%9D%D0%B8%D0%BA%D0%BE%D0%BB%D0%B0%D0%B5%D0%B2', # noqa
            'parsed_time': '31-07-2021 11:10:17',
            'source_name': 'poezdato/blablacar',
            'source_url': 'https://poezdato.net/search/get-trips2?src=%D0%9F%D0%BE%D0%BB%D1%82%D0%B0%D0%B2%D0%B0|49.603405,34.524628&dst=%D0%9D%D0%B8%D0%BA%D0%BE%D0%BB%D0%B0%D0%B5%D0%B2|46.958073,31.973779&date=31.07.2021&country=2&notrains=1&details=1&country_dst=2' # noqa
        }
    ]
}
