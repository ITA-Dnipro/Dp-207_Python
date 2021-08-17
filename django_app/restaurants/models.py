from django.db import models

class Restaurant(models.Model):
    title = models.CharField(max_length=200)
    timetable = models.CharField(max_length=100)
    # restaurant_type = models.CharField(max_length=100)
    address = models.CharField(max_length=150)
    # price_lvl = models.PositiveSmallIntegerField()
    # rating = models.FloatField(max_length=3)
    photo_href = models.CharField(max_length=200)
    city = models.CharField(max_length=100)

