from django.core.mail import send_mail
from django.template.loader import render_to_string


class OrderEmail:

    def __init__(self, order):
        self.order = order
        self.sender = 'emandruy@gmail.com'

    def topic(self):
        return f'e-mandruy заказ №{self.order.pk} получен'

    def body(self):
        context = {'order': self.order}
        return render_to_string('hotels/ordermail.txt', context)

    def send(self):
        send_mail(self.topic(), self.body(), self.sender, [self.order.user.email])
