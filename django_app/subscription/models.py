from django.db import models
from django.contrib.auth.models import User


class HotelService(models.Model):

    city = models.CharField(max_length=100)
    date_of_expire = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'city',)

    def __str__(self):
        return f'Hotel service {self.user}, {self.city}, {self.date_of_expire}'


class WeatherService(models.Model):

    city = models.CharField(max_length=100)
    date_of_expire = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'city',)

    def __str__(self):
        return f'Weather service {self.user}, {self.city}, {self.date_of_expire}'


class TransportService(models.Model):

    city_of_departure = models.CharField(max_length=100)
    city_of_arrival = models.CharField(max_length=100)
    date_of_expire = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'city_of_departure', 'city_of_arrival')

    def __str__(self):
        return f'Transport service {self.user}, {self.city}, {self.date_of_expire}'
