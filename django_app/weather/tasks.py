from celery import shared_task
from .utils.api_handler import get_weather_from_api


@shared_task()
def get_weather(city):
    data = get_weather_from_api(city)
    return data
