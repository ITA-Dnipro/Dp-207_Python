from hotels.models import Hotel, City
from django.test import TestCase
from django.core.exceptions import ValidationError
import os


class TestHotelModel(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        city = City(1)
        city.name = 'test_city'
        city.save()
        city = City.objects.get(name='test_city')
        url = 'https://vgorode.ua/img/article/3361/80_main-v1566353737.jpg'
        hotel = Hotel(name='test name',
                      adress='test_adress',
                      price='test_price',
                      details='test_details',
                      url=url,
                      contacts='test_contacts',
                      href='test_href',
                      city=city)
        hotel.save()

    def test_invalid_hotel_name(self):
        with self.assertRaises(ValidationError):
            hotel = Hotel(name='s'*151)
            hotel.full_clean()

    def test_invalid_hotel_adress(self):
        with self.assertRaises(ValidationError):
            hotel = Hotel(adress='s'*151)
            hotel.full_clean()

    def test_invalid_hotel_contacts(self):
        with self.assertRaises(ValidationError):
            hotel = Hotel(contacts='s'*151)
            hotel.full_clean()

    def test_invalid_hotel_slug(self):
        with self.assertRaises(ValidationError):
            hotel = Hotel(slug='s'*101)
            hotel.full_clean()

    def test_invalid_hotel_href(self):
        with self.assertRaises(ValidationError):
            hotel = Hotel(href='s'*101)
            hotel.full_clean()

    def test_invalid_hotel_url(self):
        with self.assertRaises(ValidationError):
            hotel = Hotel(url='s'*100)
            hotel.full_clean()

    def test_invalid_length_hotel_url(self):
        with self.assertRaises(ValidationError):
            hotel = Hotel(url='http://' + 's'*200)
            hotel.full_clean()

    def test_valid_hotel(self):
        hotel = Hotel.objects.get(name='test name')
        self.assertEqual(hotel.adress, 'test_adress')
        self.assertEqual(hotel.price, 'test_price')
        self.assertEqual(hotel.details, 'test_details')
        self.assertEqual(hotel.url, 'https://vgorode.ua/img/article/3361/80_main-v1566353737.jpg')
        self.assertEqual(hotel.contacts, 'test_contacts')
        self.assertEqual(hotel.href, 'test_href')
        self.assertEqual(hotel.city.name, 'test_city')
        self.assertEqual(hotel.slug, 'test-name')
        file = hotel.url.split('/')[-1]
        self.assertTrue(os.path.isfile(f"/usr/src/app/django_app/mediafiles/media/{file}"))

    def test_method_str(self):
        hotel = Hotel.objects.get(name='test name')
        self.assertEqual(str(hotel), 'test name')

    def test_get_absolute_url(self):
        hotel = Hotel.objects.get(name='test name')
        url = hotel.get_absolute_url()
        self.assertEqual(url, f'/hotels/hotel/%3Fhotel_id={hotel.pk}/test-name')
