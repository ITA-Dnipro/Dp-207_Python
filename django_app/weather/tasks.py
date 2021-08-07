from celery import shared_task
from .utils.api_handler import get_weather_from_api
from .models import Weather


@shared_task()
def get_weather(city):
    data = get_weather_from_api(city)
    return data


@shared_task()
def delete_all_from_weather_model():
    Weather.objects.all().delete()
