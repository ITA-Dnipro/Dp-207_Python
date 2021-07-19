from django.db import models

import datetime


class Route(models.Model):
    id = models.IntegerField(primary_key=True)
    departure_name = models.CharField(max_length=30)
    arrival_name = models.CharField(max_length=30)
    departure_date = models.DateTimeField(default=datetime.date.today)
    parsed_time = models.DateTimeField(default=datetime.date.today)
    source_name = models.CharField(max_length=350)
    source_url = models.URLField(max_length=350)


class Car(models.Model):
    id = models.IntegerField(primary_key=True)
    departure_name = models.CharField(max_length=30)
    departure_date = models.DateTimeField(default=datetime.date.today)
    arrival_name = models.CharField(max_length=30)
    price = models.CharField(max_length=20)
    car_model = models.CharField(max_length=20)
    blablacar_url = models.URLField(max_length=350)
    parsed_time = models.DateTimeField(default=datetime.date.today)
    source_name = models.CharField(max_length=350)
    source_url = models.URLField(max_length=350)


class Train(models.Model):
    id = models.IntegerField(primary_key=True)
    train_name = models.CharField(max_length=50, default=None)
    train_number = models.CharField(max_length=10)
    train_uid = models.CharField(max_length=10)
    departure_name = models.CharField(max_length=30)
    departure_code = models.IntegerField()
    departure_date = models.DateTimeField(default=datetime.date.today)
    arrival_name = models.CharField(max_length=30)
    arrival_code = models.CharField(max_length=30)
    arrival_date = models.DateTimeField(default=datetime.date.today)
    in_route_time = models.CharField(max_length=20)
    parsed_time = models.DateTimeField(default=datetime.date.today)
    source_name = models.CharField(max_length=350)
    source_url = models.URLField(max_length=350)
