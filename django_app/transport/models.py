from django.db import models


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
