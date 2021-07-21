from django.db import models

import datetime


class Route(models.Model):
    departure_name = models.CharField(max_length=300)
    arrival_name = models.CharField(max_length=300)
    departure_date = models.DateTimeField(default=datetime.date.today, null=True)
    parsed_time = models.DateTimeField(default=datetime.date.today, null=True)
    source_name = models.CharField(max_length=500)
    source_url = models.URLField(max_length=500)


class Car(models.Model):
    route_id = models.ForeignKey(Route, on_delete=models.CASCADE)
    departure_name = models.CharField(max_length=300)
    departure_date = models.DateTimeField(default=datetime.date.today, null=True)
    arrival_name = models.CharField(max_length=300)
    price = models.CharField(max_length=200)
    car_model = models.CharField(max_length=200)
    blablacar_url = models.URLField(max_length=500)
    parsed_time = models.DateTimeField(default=datetime.date.today, null=True)
    source_name = models.CharField(max_length=500)
    source_url = models.URLField(max_length=500)


class Train(models.Model):
    route_id = models.ForeignKey(Route, on_delete=models.CASCADE)
    train_name = models.CharField(max_length=300, default=None)
    train_number = models.CharField(max_length=200)
    train_uid = models.CharField(max_length=200)
    departure_name = models.CharField(max_length=300)
    departure_code = models.IntegerField()
    departure_date = models.DateTimeField(default=datetime.date.today, null=True)
    arrival_name = models.CharField(max_length=300)
    arrival_code = models.CharField(max_length=300)
    arrival_date = models.DateTimeField(default=datetime.date.today, null=True)
    in_route_time = models.CharField(max_length=200)
    parsed_time = models.DateTimeField(default=datetime.date.today, null=True)
    source_name = models.CharField(max_length=500)
    source_url = models.URLField(max_length=500)
