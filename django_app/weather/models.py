from django.db import models


class Weather(models.Model):
    city = models.ForeignKey('hotels.City', on_delete=models.CASCADE)
    current_temp = models.FloatField()
    max_temp = models.FloatField()
    min_temp = models.FloatField()
    feels_like = models.FloatField(blank=True)
    description = models.CharField(max_length=100)
    humidity = models.FloatField()
    wind = models.FloatField()
    clouds = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    current_date = models.DateTimeField()
    icon = models.CharField(max_length=100)
