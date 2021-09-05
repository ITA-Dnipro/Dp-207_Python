from django.db import models
from django.contrib.auth.models import User


class CustonException(Exception):

    def __init__(self, msg):
        self.msg = msg


class NotUniqueSubscription(CustonException):
    pass


class Subscription(models.Model):

    service = models.CharField(max_length=100)
    city_of_departure = models.CharField(max_length=100, blank=True)
    target_city = models.CharField(max_length=100)
    date_of_expire = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Subscription on {self.service} by {self.user}, info: {self.target_city}, {self.city_of_departure}, {self.date_of_expire}'

    def save(self):
        subs = self.__class__.objects.filter(user=self.user)
        if not subs:
            return super().save()
        for sub in subs:
            if sub.service == self.service and sub.target_city == self.target_city \
                        and sub.user == self.user and sub.city_of_departure == self.city_of_departure:
                raise NotUniqueSubscription(f"Subscription on {self.service} in {self.target_city} {self.city_of_departure} is already exist")
            else:
                return super().save()

    def update(self):
        return super().save()
