from .api_handler import get_data_for_hotels_by_city
from .models_handler import CityModel, HotelModel, HotelCommentModel, \
    RatingModel, OrderModel
from django.contrib.auth.models import User
from ..models import Rating


# creates cities and hotels in db
class CityAndHotelsHandler:
    def __init__(self, city_name):
        self.city = CityModel(city_name)
        self.hotel = HotelModel()

    # takes data from parsing and create objects
    def get_data_from_api_and_create_models(self):

        city = self.city.get_city_by_name()
        if not city:

            data = get_data_for_hotels_by_city(self.city.city_name)
            city = self.city.create_city()
            for hotel_ in data:
                self.hotel.create_hotel(hotel_name=hotel_['hotel_name'],
                                        adress=hotel_['adress'],
                                        prices=hotel_['prices'],
                                        detail=hotel_['detail'],
                                        photo=hotel_['photo'],
                                        contacts=hotel_['contacts'],
                                        href=hotel_['href'],
                                        city=city)
        else:
            hotels_for_city = city.hotel_set.all()
            if not hotels_for_city:
                data = get_data_for_hotels_by_city(self.city.city_name)
                city = self.city.create_city()
                for hotel_ in data:
                    self.hotel.create_hotel(hotel_name=hotel_['hotel_name'],
                                            adress=hotel_['adress'],
                                            prices=hotel_['prices'],
                                            detail=hotel_['detail'],
                                            photo=hotel_['photo'],
                                            contacts=hotel_['contacts'],
                                            href=hotel_['href'],
                                            city=city)
        return True


# create comments class
class CreateComment:

    # init objects
    def __init__(self, pk, request):
        self.object = HotelModel()
        self.pk = pk
        self.request = request

    # create a comment to this object
    def create_comment(self):
        hotel = self.object.get_hotel_by_pk(self.pk)
        try:
            text = self.request.POST.get('text')
            author = self.request.POST.get('author')
            if text and author:
                comment = HotelCommentModel()
                comment.create_comment(hotel=hotel,
                                       text=text, author=author)
                return hotel
        except TypeError:
            print('Problem with creating new comment')


# creates rating for object
class CreateRating:

    # init object
    def __init__(self, pk, request):
        self.object = HotelModel()
        self.pk = pk
        self.request = request

    # create rating for object
    def create_rating(self):
        hotel = self.object.get_hotel_by_pk(self.pk)
        user = User.objects.filter(pk=self.request.user.pk).first()
        try:
            mark = self.request.POST.get('mark')
            if mark:
                rate = RatingModel()
                rate.create_rating(hotel=hotel,
                                   mark=mark,
                                   user=user)
                return hotel
        except TypeError:
            print('Problem with creating new comment')

    # we check here if authenticated user already rated this hotel
    def check_is_hotel_rated_by_user(self):
        hotel = self.object.get_hotel_by_pk(self.pk)
        user = User.objects.filter(pk=self.request.user.pk).first()
        is_rated = Rating.objects.filter(hotel=hotel).filter(user=user).first()

        if is_rated:
            return True

        return False


class CreateOrder:

    def __init__(self, request, slug, check_in, check_out, user, price):
        self.object = OrderModel()
        self.hotel = HotelModel()
        self.request = request
        self.hotel_slug = slug
        self.check_in = check_in
        self.check_out = check_out
        self.user = user
        self.price = price

    def create_order(self):
        hotel = self.hotel.get_hotel_by_slug(self.hotel_slug)

        order = self.object.create_order(hotel=hotel, user=self.user, check_in=self.check_in,
                                         check_out=self.check_out, price=self.get_price_in_int())

        return order

    def get_price_in_int(self):

        price = ''

        for i in self.price:
            if i.isdigit():
                price += i

        return int(price)
