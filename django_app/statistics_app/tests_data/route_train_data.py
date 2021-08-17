import datetime
import pytz

route_trains_data = {
    'trains_data': {
        'id': 19,
        'departure_name': 'Киев',
        'arrival_name': 'Львов',
        'departure_date': datetime.datetime(2021, 8, 16, 21, 0, tzinfo=pytz.utc),
        'parsed_time': datetime.datetime(2021, 8, 16, 10, 15, 18, tzinfo=pytz.utc),
        'source_name': 'poezd.ua',
        'source_url': 'https://poezd.ua/zd',
        'trips': [
            {
                'id': 51,
                'route_id_id': 19,
                'train_name': 'ВЛАДИСЛАВ ЗУБЕНКО',
                'train_number': '015О',
                'train_uid': '015О',
                'departure_name': 'Харьков',
                'departure_code': 2204001,
                'departure_date': datetime.datetime(2021, 8, 16, 22, 18, tzinfo=pytz.utc),
                'arrival_name': 'Львов', 'arrival_code': 2218000,
                'arrival_date': datetime.datetime(2021, 8, 17, 4, 39, tzinfo=pytz.utc),
                'in_route_time': '6 ч 21 мин',
                'parsed_time': datetime.datetime(2021, 8, 16, 10, 15, 18, tzinfo=pytz.utc),
                'source_name': 'poezd.ua',
                'source_url': 'https://poezd.ua/zd'
            }
        ],
        'result': True
    }
}
search_route_train_data = {
    'departure_name': route_trains_data['trains_data']['departure_name'],
    'arrival_name': route_trains_data['trains_data']['arrival_name'],
    'departure_date': '17.08.2021',
    'transport_types': 'train',
}
