from celery import shared_task
from .email.email import OrderEmail
from .models import Order
from .utils.api_handler import send_msg


@shared_task
def send_order_email(order_pk):
    order = Order.objects.get(pk=order_pk)
    mail = OrderEmail(order=order)
    mail.send()
    return True


@shared_task
def send_new_order_msg_to_tg(order_pk):
    order = Order.objects.get(pk=order_pk)
    text = f'Поступил новый заказ {order.pk}\n{order.hotel.name}\n' \
           f'от {order.user.username}'
    send_msg(text)
    return True
