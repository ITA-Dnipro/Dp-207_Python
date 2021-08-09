from ..models import City, Hotel, HotelComment, Rating, Order


class CityModel:

    def __init__(self, city_name):
        self.city_name = city_name

    def create_city(self):
        city = City.objects.filter(name=self.city_name).first()
        if not city:
            city = City(name=self.city_name)
            city.save()
            return city
        return city

    def get_city_by_name(self):
        city = City.objects.filter(name=self.city_name).first()
        if not city:
            return False
        return city


class HotelModel:

    # create hotel method
    def create_hotel(self, hotel_name, adress, prices,
                     detail, photo, contacts, city, href):
        hotel = Hotel.objects.filter(name=hotel_name).first()

        if not hotel:
            new_hotel = Hotel(name=hotel_name,
                              adress=adress,
                              price=prices,
                              details=detail,
                              url=photo,
                              contacts=contacts,
                              href=href,
                              city=city)
            new_hotel.save()
        return True

    # get get hotel object by pk
    def get_hotel_by_pk(self, pk):
        hotel = Hotel.objects.get(pk=pk)
        if not hotel:
            return False
        return hotel

    def get_hotel_by_slug(self, slug):
        hotel = Hotel.objects.get(slug=slug)
        if not hotel:
            return False
        return hotel

    # getting all hotels by city
    def get_all_hotels_by_city(self, city):
        city = City.objects.filter(name=city).first()
        return Hotel.objects.filter(city=city).all()

    # getting all hotels from db
    def get_all_hotels(self):
        return Hotel.objects.all()

    # sort hotels by avg rating
    def sort_hotels_by_avg_rating(self, hotels=None, reverse=True):
        # if reverse sorting will be from top to bottom
        if reverse:
            return sorted(hotels,
                          key=lambda x: -x.get_avg_marks())
        else:
            return sorted(hotels,
                          key=lambda x: x.get_avg_marks())


class HotelCommentModel:

    def create_comment(self, **kwargs):
        new_comment = HotelComment(**kwargs)
        new_comment.save()


class RatingModel:

    def create_rating(self, **kwargs):
        new_rate = Rating(**kwargs)
        new_rate.save()


class OrderModel:

    def create_order(self, **kwargs):
        new_order = Order(**kwargs)
        new_order.save()
        return new_order
