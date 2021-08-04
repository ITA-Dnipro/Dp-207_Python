from django.db import models
from django.utils import timezone


class Weather(models.Model):
    temperature = models.FloatField()
    feels_like = models.FloatField()
    description = models.CharField(max_length=100)
    humidity = models.FloatField()
    wind = models.FloatField()
    clouds = models.FloatField()
    city = models.CharField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)
