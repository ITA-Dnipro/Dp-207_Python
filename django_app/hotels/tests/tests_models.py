from hotels.models import Hotel, City, HotelComment, Order
from django.test import TestCase
from django.core.exceptions import ValidationError
import os
# from unittest import mock
from .fixture import CITY_EXISTS, API_RESULT_FOR_HOTELS_IN_THE_CITY, CHECK_IN, CHECK_OUT, PRICE, TIME
from hotels.utils.models_handler import CityModel, HotelModel
from django.contrib.auth.models import User


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

    def test_get_rooms(self):
        hotel = Hotel(price=f'{{"price":"{PRICE}"}}')
        self.assertEqual(hotel.get_rooms(), {"price": f'{PRICE}'})


def mock_time(time):
    class MockTime():

        def __init__(self):
            self.time = '2021-08-11 12:18'

        def strftime(self, template):
            return self.time

    return MockTime()


class TestHotelComment(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        city = CityModel(city_name=CITY_EXISTS).create_city()
        data = API_RESULT_FOR_HOTELS_IN_THE_CITY[0][0]
        data['city'] = city
        HotelModel().create_hotel(**data)
        cls.hotel = Hotel.objects.all().first()
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        cls.user = user

    def test_method_str(self):
        comment = HotelComment(hotel=self.hotel, text='some text', author=self.user)
        comment.get_localtime = mock_time
        self.assertEqual(str(comment), f'"some text" by (john) ({TIME})')


class TestOrder(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        city = CityModel(city_name=CITY_EXISTS).create_city()
        data = API_RESULT_FOR_HOTELS_IN_THE_CITY[0][0]
        data['city'] = city
        HotelModel().create_hotel(**data)
        cls.hotel = Hotel.objects.all().first()
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        cls.user = user

    def test_method_str(self):
        order = Order(hotel=self.hotel, check_out=CHECK_OUT, check_in=CHECK_IN, user=self.user, price=PRICE[:-4])
        order.get_localtime = mock_time
        self.assertEqual(str(order), f'Order made at {TIME}')