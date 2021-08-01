from datetime import datetime, timedelta

train_route_departure_date = datetime.now().strftime("%d.%m.%Y")
train_route_departure_date_response_format = (
    datetime.now().strftime("%d-%m-%Y")
)
train_departure_date_in_future = datetime.now() + timedelta(minutes=5)
train_departure_date_in_future_response_format = (
    train_departure_date_in_future.strftime("%d-%m-%Y %H:%M:%S")
)
train_departure_date_in_future_db_format = (
    f'{train_departure_date_in_future.strftime("%Y-%m-%d %H:%M:%S")}'
)

route_train = {
    'result': True,
    'departure_name': 'Киев',
    'departure_date': f'{train_route_departure_date}',
    'arrival_name': 'Одесса',
    'parsed_time': f'{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}',
    'source_name': 'poezd.ua',
    'source_url': 'https://poezd.ua/zd',
    'trips': [
        {
            'train_name': 'Интерсити',
            'train_number': '761К',
            'train_uid': '761K_0_2',
            'departure_name': 'Киев',
            'departure_code': 2200001,
            'departure_date': (
                train_departure_date_in_future_db_format
            ),
            'arrival_name': 'Одесса',
            'arrival_code': 2208001,
            'arrival_date': '2021-08-05 14:01:00',
            'in_route_time': '7 ч 46 мин',
            'parsed_time': '31-07-2021 20:15:01',
            'source_name': 'poezd.ua',
            'source_url': 'https://poezd.ua/zd'
        }
    ]
}
