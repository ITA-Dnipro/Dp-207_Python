from django.db import models


# Create your models here.
class Weather(models.Model):
    temperature = models.FloatField()
    feels_like = models.FloatField()
    description = models.CharField(max_length=100)
    humidity = models.FloatField()
    wind = models.FloatField()
    clouds = models.FloatField()
    city = models.ForeignKey("hotels.City", on_delete=models.CASCADE)
