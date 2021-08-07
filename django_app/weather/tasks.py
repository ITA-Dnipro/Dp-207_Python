from celery import shared_task
from .utils.api_handler import get_weather_from_api
<<<<<<< HEAD
from .models import Weather
=======
>>>>>>> eb98306e32aac26e2ab1251989a84a391d121dd3


@shared_task()
def get_weather(city):
    data = get_weather_from_api(city)
    return data
<<<<<<< HEAD


@shared_task()
def delete_all_from_weather_model():
    Weather.objects.all().delete()
=======
>>>>>>> eb98306e32aac26e2ab1251989a84a391d121dd3
