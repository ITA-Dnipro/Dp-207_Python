from django.db import models
from django.db.models import Avg, F
from django.urls import reverse
from django.core.files import File
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from urllib.request import urlretrieve

import pytz
import os

RATING_CHOICE = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]

# create City model
class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.name}'


# create Hotel model
class Hotel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    adress = models.CharField(max_length=150)
    price = models.TextField()
    details = models.TextField()
    photo = models.ImageField(upload_to='media', blank=True)
    url = models.URLField(max_length=200)
    contacts = models.CharField(max_length=50)
    # relation with city
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    # override save method to save images from url
    def save(self, *args, **kwargs):
        if self.url and not self.photo:
            result = urlretrieve(str(self.url))
            self.photo.save(
                os.path.basename(str(self.url)),
                File(open(result[0], 'rb'))
            )
        super(Hotel, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('hotels:hotel_detail', args=(self.pk,))

    def __str__(self):
        return f'{self.name}'

    # method to get avg rating for each hotel
    def get_avg_marks(self):
        rates = self.rating_set.all()
        if not rates:
            return 0.0
        return round(self.rating_set.all().aggregate(Avg('mark'))['mark__avg'], 1)


# create class for comment model
class HotelComment(models.Model):
    # relation with hotel
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE,
                              related_name='comments')
    text = models.TextField()
    author = models.CharField(max_length=50)
    date_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        dt = self.get_localtime(self.date_time).strftime('%d.%m.%y %H:%M')
        return f'"{self.text}" by ({self.author}) ({dt})'

    class Meta:
        ordering = ['-date_time']

    # get local time
    @staticmethod
    def get_localtime(utctime):
        utc = utctime.replace(tzinfo=pytz.UTC)
        localtz = utc.astimezone(timezone.get_current_timezone())
        return localtz


# create class for Rating model
class Rating(models.Model):
    mark = models.FloatField(null=True, blank=True, choices=RATING_CHOICE, validators=[MinValueValidator(0),
                                       MaxValueValidator(10)])
    # relation with hotel
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)

