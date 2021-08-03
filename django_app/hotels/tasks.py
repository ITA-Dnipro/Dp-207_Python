from celery import shared_task
from .email.email import OrderEmail
from .models import Order


@shared_task
def send_order_email(order_pk):
    order = Order.objects.get(pk=order_pk)
    mail = OrderEmail(order=order)
    mail.send()
    return True
