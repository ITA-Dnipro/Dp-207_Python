from celery import shared_task, chain
from weather.utils.api_handler import get_weather_from_api
from subscription.models import Subscription
from django.utils import timezone
from django.core.mail import send_mail
from hotels.utils.api_handler import get_data_for_hotels_by_city
from django.template.loader import render_to_string
from services.transport_app.view_utils.view_helpers import get_route_data
import json
from subscription.utils.utils_for_tasks import create_task
from collections import defaultdict


@shared_task()
def get_subscriptons():
    subscriptons = list(Subscription.objects.select_related('user').filter(date_of_expire__gt=timezone.now()))
    tasks = create_task(subscriptons)
    return tasks


@shared_task()
def get_data_from_api(subs):
    for sub in subs:
        if sub["service"] == "weather":
            sub["data"] = get_weather_from_api(sub['target_city'])
        elif sub["service"] == "hotels":
            sub["data"] = get_data_for_hotels_by_city(sub['target_city'])
        elif sub["service"] == "transport":
            payload = {"departure_name": sub["city_of_departure"],
                       "arrival_name": sub["target_city"],
                       "departure_date": timezone.now().strftime("%d.%m.%Y"),
                       "transport_types": ["car"]}
            sub["data"] = get_route_data(payload)
    return subs


@shared_task()
def form_context(subs):
    context = defaultdict(list)
    for sub in subs:
        context[sub["service"]].append(sub)
    return context


@shared_task()
def send_email(context, key):
    user = json.loads(key)
    context["name"] = user["name"]
    send_mail('Subscriptions', render_to_string('subscription/letter.txt', context), 'emandruy@gmail.com', [user["email"]])


@shared_task()
def sending_emails():
    for key, subs in get_subscriptons().items():
        flow = chain(get_data_from_api.s(subs), form_context.s(), send_email.s(key))
        flow()
