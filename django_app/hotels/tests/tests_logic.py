from django.test import TestCase
from hotels.utils.logic import CityAndHotelsHandler, CreateComment, CreateRating, CreateOrder
from unittest import mock
from .fixture import API_RESULT_FOR_HOTELS_IN_THE_CITY, CITY_EXISTS, CHECK_IN, CHECK_OUT, PRICE
from hotels.models import City, Hotel, HotelComment, Rating
from hotels.utils.models_handler import CityModel, HotelModel
from django.contrib.auth.models import User


class TestHotelModel(TestCase):

    @mock.patch('hotels.utils.logic.get_data_for_hotels_by_city', side_effect=API_RESULT_FOR_HOTELS_IN_THE_CITY)
    def test_get_data_from_api_and_create_models(self, mock, city_name=CITY_EXISTS):
        with self.assertRaises(City.DoesNotExist):
            City.objects.get(name=CITY_EXISTS)
        instance = CityAndHotelsHandler(city_name)
        instance.get_data_from_api_and_create_models()
        self.assertTrue(City.objects.get(name=CITY_EXISTS))
        self.assertEqual(len(Hotel.objects.all()), 1)

    @mock.patch('hotels.utils.logic.get_data_for_hotels_by_city', side_effect=API_RESULT_FOR_HOTELS_IN_THE_CITY)
    def test_get_data_from_api_and_create_models_with_city_in_db(self, mock, city_name=CITY_EXISTS):
        instance = CityAndHotelsHandler(city_name)
        instance.city.create_city()
        self.assertTrue(City.objects.get(name=CITY_EXISTS))
        instance.get_data_from_api_and_create_models()
        self.assertEqual(len(Hotel.objects.all()), 1)

    @mock.patch('hotels.utils.logic.get_data_for_hotels_by_city', side_effect=API_RESULT_FOR_HOTELS_IN_THE_CITY)
    def test_get_data_from_api_and_create_models_with_city_and_hotel_in_db(self, mock, city_name=CITY_EXISTS):
        instance = CityAndHotelsHandler(city_name)
        city = instance.city.create_city()
        data = API_RESULT_FOR_HOTELS_IN_THE_CITY[0][0]
        data['city'] = city
        instance.hotel.create_hotel(**data)
        self.assertTrue(City.objects.get(name=CITY_EXISTS))
        instance.get_data_from_api_and_create_models()
        self.assertEqual(len(Hotel.objects.all()), 1)
        self.assertEqual(mock.call_count, 0)

    def tearDown(self):
        City.objects.all().delete()
        Hotel.objects.all().delete()


def mocked_request_for_creating_comment_and_rating():
    class MockRequest:

        def __init__(self):
            class MockUser():

                def __init__(self, pk):
                    self.pk = User.objects.all()[0].pk

            class MockPost():

                def get(self, text):
                    if text == 'text':
                        return 'test text'
                    elif text == 'mark':
                        return 5
            self.user = MockUser(1)
            self.POST = MockPost()

    return MockRequest()


class TestCreateComment(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        city = CityModel(city_name=CITY_EXISTS).create_city()
        data = API_RESULT_FOR_HOTELS_IN_THE_CITY[0][0]
        data['city'] = city
        HotelModel().create_hotel(**data)
        User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def test_create_comment(self):
        request = mocked_request_for_creating_comment_and_rating()
        pk = Hotel.objects.all().first().pk
        instance = CreateComment(pk, request)
        instance.create_comment()
        self.assertEqual(HotelComment.objects.all().first().text, request.POST.get('text'))
        self.assertEqual(HotelComment.objects.all().first().hotel.pk, pk)
        self.assertEqual(HotelComment.objects.all().first().author.pk, request.user.pk)


class TestCreateRating(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        city = CityModel(city_name=CITY_EXISTS).create_city()
        data = API_RESULT_FOR_HOTELS_IN_THE_CITY[0][0]
        data['city'] = city
        HotelModel().create_hotel(**data)
        User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def test_create_rating(self):
        request = mocked_request_for_creating_comment_and_rating()
        pk = Hotel.objects.all().first().pk
        instance = CreateRating(pk, request)
        instance.create_rating()
        self.assertEqual(Rating.objects.all().first().mark, request.POST.get('mark'))
        self.assertEqual(Rating.objects.all().first().hotel.pk, pk)
        self.assertEqual(Rating.objects.all().first().user.pk, request.user.pk)

    def test_check_is_hotel_rated_by_user(self):
        request = mocked_request_for_creating_comment_and_rating()
        pk = Hotel.objects.all().first().pk
        instance = CreateRating(pk, request)
        instance.create_rating()
        self.assertTrue(instance.check_is_hotel_rated_by_user())

    def test_check_is_not_hotel_rated_by_user(self):
        request = mocked_request_for_creating_comment_and_rating()
        pk = Hotel.objects.all().first().pk
        instance = CreateRating(pk, request)
        self.assertFalse(instance.check_is_hotel_rated_by_user())


class TestCreateOrder(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        city = CityModel(city_name=CITY_EXISTS).create_city()
        data = API_RESULT_FOR_HOTELS_IN_THE_CITY[0][0]
        data['city'] = city
        HotelModel().create_hotel(**data)
        User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        cls.hotel = Hotel.objects.all().first()
        cls.slug = cls.hotel.slug
        cls.request = mocked_request_for_creating_comment_and_rating()
        cls.check_in = CHECK_IN
        cls.check_out = CHECK_OUT
        cls.user = User.objects.all().first()
        cls.price = PRICE
        cls.instance = CreateOrder(request=cls.request, slug=cls.slug, check_in=cls.check_in,
                                   check_out=cls.check_out, user=cls.user, price=cls.price)

    def test_create_order(self):
        order = self.instance.create_order()
        self.assertEqual(order.hotel, self.hotel)
        self.assertEqual(order.check_in, CHECK_IN)
        self.assertEqual(order.check_out, CHECK_OUT)
        self.assertEqual(order.price, int(self.price[:-4]))
        self.assertEqual(order.user, self.user)

    def test_get_price_in_int(self):
        self.assertEqual(self.instance.get_price_in_int(), int(self.price[:-4]))
