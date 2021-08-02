from celery import shared_task
from .models import City
import random


@shared_task
def send_order_email(mail):
    mail.send()
