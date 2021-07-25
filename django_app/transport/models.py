from django.db import models
# from django.utils import timezone
from datetime import datetime
import pytz


class Route(models.Model):
    departure_name = models.CharField(max_length=300)
    arrival_name = models.CharField(max_length=300)
    departure_date = models.DateTimeField(null=True, blank=True)
    parsed_time = models.DateTimeField(null=True, blank=True)
    source_name = models.CharField(max_length=350)
    source_url = models.URLField(max_length=1350)

    def __str__(self):
        return (
            f'{self.pk} - {self.departure_name} - {self.arrival_name} - '
            f'{self.source_name} - {self.departure_date}'
        )

    def save(self, *args, **kwargs):
        '''
        Saving Route model method
        '''
        if self.departure_date:
            self.departure_date = datetime.strptime(
                self.departure_date, '%d.%m.%Y'
            )
            self.departure_date = pytz.timezone('Europe/Kiev').localize(
                self.departure_date, is_dst=True
            )
            self.departure_date = (
                self.departure_date.astimezone(pytz.timezone('UTC'))
            )
        if self.parsed_time:
            self.parsed_time = datetime.strptime(
                self.parsed_time, '%d-%m-%Y %H:%M:%S'
            )
            #
            self.parsed_time = pytz.timezone('Europe/Kiev').localize(
                self.parsed_time, is_dst=True
            )
            self.parsed_time = (
                self.parsed_time.astimezone(pytz.timezone('UTC'))
            )
        super(Route, self).save(*args, **kwargs)


class Car(models.Model):
    route_id = models.ForeignKey(
        Route, on_delete=models.CASCADE
    )
    departure_name = models.CharField(max_length=300)
    departure_date = models.DateTimeField(null=True)
    arrival_name = models.CharField(max_length=300)
    price = models.CharField(max_length=200)
    car_model = models.CharField(max_length=200, blank=True, null=True)
    blablacar_url = models.URLField(max_length=350)
    parsed_time = models.DateTimeField(null=True)
    source_name = models.CharField(max_length=350)
    source_url = models.URLField(max_length=1350)

    def __str__(self):
        return (
            f'{self.pk} - {self.departure_name} - {self.arrival_name} - '
            f'{self.departure_date}'
        )

    def save(self, *args, **kwargs):
        '''
        Saving Car model method
        '''
        if self.departure_date:
            self.departure_date = datetime.strptime(
                self.departure_date, '%d/%m/%Y %H:%M:%S'
            )
            self.departure_date = pytz.timezone('Europe/Kiev').localize(
                self.departure_date, is_dst=True
            )
            self.departure_date = (
                self.departure_date.astimezone(pytz.timezone('UTC'))
            )
        if self.parsed_time:
            self.parsed_time = datetime.strptime(
                self.parsed_time, '%d-%m-%Y %H:%M:%S'
            )
            #
            self.parsed_time = pytz.timezone('Europe/Kiev').localize(
                self.parsed_time, is_dst=True
            )
            self.parsed_time = (
                self.parsed_time.astimezone(pytz.timezone('UTC'))
            )
        super(Car, self).save(*args, **kwargs)


class Train(models.Model):
    # id = models.IntegerField(primary_key=True)
    route_id = models.ForeignKey(
        Route, on_delete=models.CASCADE
    )
    train_name = models.CharField(max_length=300, null=True, blank=True)
    train_number = models.CharField(max_length=200)
    train_uid = models.CharField(max_length=200)
    departure_name = models.CharField(max_length=300)
    departure_code = models.IntegerField(null=True)
    departure_date = models.DateTimeField(null=True, blank=True)
    arrival_name = models.CharField(max_length=300)
    arrival_code = models.IntegerField(null=True)
    arrival_date = models.DateTimeField(null=True, blank=True)
    in_route_time = models.CharField(max_length=200)
    parsed_time = models.DateTimeField(null=True, blank=True)
    source_name = models.CharField(max_length=350)
    source_url = models.URLField(max_length=1350)

    def __str__(self):
        return (
            f'{self.pk} - {self.train_number} - {self.departure_name} - '
            f'{self.arrival_name} - {self.departure_date}'
        )

    def save(self, *args, **kwargs):
        '''
        Saving Train model method
        '''
        if self.departure_date:
            self.departure_date = datetime.strptime(
                self.departure_date, '%Y-%m-%d %H:%M:%S'
            )
            self.departure_date = pytz.timezone('Europe/Kiev').localize(
                self.departure_date, is_dst=True
            )
            self.departure_date = (
                self.departure_date.astimezone(pytz.timezone('UTC'))
            )
        if self.arrival_date:
            self.arrival_date = datetime.strptime(
                self.arrival_date, '%Y-%m-%d %H:%M:%S'
            )
            self.arrival_date = pytz.timezone('Europe/Kiev').localize(
                self.arrival_date, is_dst=True
            )
            self.arrival_date = (
                self.arrival_date.astimezone(pytz.timezone('UTC'))
            )
        if self.parsed_time:
            self.parsed_time = datetime.strptime(
                self.parsed_time, '%d-%m-%Y %H:%M:%S'
            )
            #
            self.parsed_time = pytz.timezone('Europe/Kiev').localize(
                self.parsed_time, is_dst=True
            )
            self.parsed_time = (
                self.parsed_time.astimezone(pytz.timezone('UTC'))
            )
        super(Train, self).save(*args, **kwargs)
