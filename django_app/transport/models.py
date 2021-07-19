from django.db import models

import datetime


class Route(models.Model):
    id = models.IntegerField(primary_key=True)
    departure_name = models.CharField(max_length=300)
    arrival_name = models.CharField(max_length=300)
    departure_date = models.DateTimeField(default=datetime.date.today)
    parsed_time = models.DateTimeField(default=datetime.date.today)
    source_name = models.CharField(max_length=350)
    source_url = models.URLField(max_length=350)


class Car(models.Model):
    id = models.IntegerField(primary_key=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="car")
    departure_name = models.CharField(max_length=300)
    departure_date = models.DateTimeField(default=datetime.date.today)
    arrival_name = models.CharField(max_length=300)
    price = models.CharField(max_length=200)
    car_model = models.CharField(max_length=200)
    blablacar_url = models.URLField(max_length=350)
    parsed_time = models.DateTimeField(default=datetime.date.today)
    source_name = models.CharField(max_length=350)
    source_url = models.URLField(max_length=350)


class Train(models.Model):
    id = models.IntegerField(primary_key=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="train")
    train_name = models.CharField(max_length=300, default=None)
    train_number = models.CharField(max_length=200)
    train_uid = models.CharField(max_length=200)
    departure_name = models.CharField(max_length=300)
    departure_code = models.IntegerField()
    departure_date = models.DateTimeField(default=datetime.date.today)
    arrival_name = models.CharField(max_length=300)
    arrival_code = models.CharField(max_length=300)
    arrival_date = models.DateTimeField(default=datetime.date.today)
    in_route_time = models.CharField(max_length=200)
    parsed_time = models.DateTimeField(default=datetime.date.today)
    source_name = models.CharField(max_length=350)
    source_url = models.URLField(max_length=350)
