from transport.models import Route
from datetime import datetime, timedelta
import pytz


def is_route_exists(payload, source_name):
    '''
    Return True if route exists
    '''
    db_payload = dict(payload)
    db_payload = model_query_time_converter(db_payload)
    route = Route.objects.filter(
        departure_name=db_payload['departure_name'],
        departure_date=db_payload['departure_date'],
        arrival_name=db_payload['arrival_name'],
        source_name=source_name
    ).first()
    if route:
        return True
    return False


def is_route_parsed_1_hour_ago(payload, source_name):
    '''
    Return True if route parsed_time <= than 1 hour
    '''
    db_payload = dict(payload)
    db_payload = model_query_time_converter(db_payload)
    route = Route.objects.filter(
        departure_name=db_payload['departure_name'],
        departure_date=db_payload['departure_date'],
        arrival_name=db_payload['arrival_name'],
        source_name=source_name
    ).first()
    #
    one_hour_delta = timedelta(hours=1)
    #
    now_time = datetime.utcnow().replace(tzinfo=pytz.utc)
    #
    route_parsed_time_diff = now_time - route.parsed_time
    #
    if route_parsed_time_diff <= one_hour_delta:
        return False
    else:
        return True


def model_query_time_converter(db_payload):
    '''
    Return payload dict with payload['departure_date'] converted
    to datetime object with proper timezone
    '''
    db_payload['departure_date'] = datetime.strptime(
        db_payload['departure_date'], '%d.%m.%Y'
    )
    db_payload['departure_date'] = pytz.timezone(
        'Europe/Kiev'
    ).localize(
        db_payload['departure_date'], is_dst=True
    )
    db_payload['departure_date'] = (
        db_payload['departure_date'].astimezone(pytz.timezone('UTC'))
    )
    return db_payload
