from django.urls import path
from .views import main_page, hotels_by_city, HotelDetailView, \
    hotel_comment, create_rating, get_free_rooms_for_hotels, order_room


app_name = 'hotels'
urlpatterns = [
    path('main', main_page, name='main'),
    path('отели_<str:city_name>/', hotels_by_city, name='hotels_list'),
    path('hotel/?hotel_id=<int:pk>/<str:slug>', HotelDetailView.as_view(), name='hotel_detail'),
    path('hotel/comment/<int:pk>', hotel_comment, name='hotel_comment'),
    path('hotel/ratings/<int:pk>', create_rating, name='rating_create'),
    path('hotel/<str:slug>/rooms/?check_in=<str:check_in>/?check_out=<str:check_out>',
         get_free_rooms_for_hotels, name='free_rooms'),
    path('hotel/<str:slug>/room/ordered/?check_in=<str:check_in>/?check_out=<str:check_out>/<str:price>/<delta_days>',
         order_room, name='order_room')
]
