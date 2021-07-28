from django.db import models
from django.db.models import Avg
from django.urls import reverse
from django.core.files import File
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.utils.text import slugify
from urllib.request import urlretrieve
import pytz
import os


# rating choice options for hotels
RATING_CHOICE = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]


# create City model
class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.name}'


# create Hotel model
class Hotel(models.Model):
    """
    Hotel model with it fields and has FK to City
    """
    name = models.CharField(max_length=150, unique=True)
    adress = models.CharField(max_length=150)
    price = models.TextField()
    details = models.TextField()
    photo = models.ImageField(upload_to='media', blank=True)
    url = models.URLField(max_length=200)
    contacts = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, max_length=100)

    # relation with city
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    # override save method to save images from url
    # and save custom slug
    def save(self, *args, **kwargs):

        # making slug
        self.slug = slugify(self.name, allow_unicode=True)

        # getting image
        if self.url and not self.photo:
            result = urlretrieve(str(self.url))
            self.photo.save(
                os.path.basename(str(self.url)),
                File(open(result[0], 'rb'))
            )

        super(Hotel, self).save(*args, **kwargs)

    # getting url for reverse
    def get_absolute_url(self):
        return reverse('hotels:hotel_detail', args=(self.pk, self.slug))

    def __str__(self):
        return f'{self.name}'

    # method to get avg rating for each hotel
    def get_avg_marks(self):
        rates = self.rating_set.all()
        if not rates:
            return 0.0
        return round(self.rating_set.all().aggregate(
            Avg('mark'))['mark__avg'], 1)

    # get rooms from self.price field for better display in template
    def get_rooms(self):
        rooms = eval(str(self.price))
        return rooms


# create class for comment model
class HotelComment(models.Model):
    """
    HottelComment class with it fields and has FK to Hotel model
    """
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
    mark = models.FloatField(null=True, blank=True, choices=RATING_CHOICE,
                             validators=[MinValueValidator(0),
                                         MaxValueValidator(10)])
    # relation with hotel
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Order(models.Model):
    """
    Order class with date fields and has FK to Hotel model
    """
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    order_time = models.DateTimeField(default=timezone.now)
    check_in = models.CharField(max_length=30)
    check_out = models.CharField(max_length=30)
    price = models.IntegerField()

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        dt = self.get_localtime(self.order_time).strftime('%d.%m.%Y %H:%M')
        return f'"Order made at {dt}'

    # get local time
    @staticmethod
    def get_localtime(utctime):
        utc = utctime.replace(tzinfo=pytz.UTC)
        localtz = utc.astimezone(timezone.get_current_timezone())
        return localtz
