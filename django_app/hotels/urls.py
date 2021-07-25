from django.urls import path
from .views import main_page, hotels_by_city, HotelDetailView, \
    hotel_comment, create_rating, create_order


app_name = 'hotels'
urlpatterns = [
    path('main', main_page, name='main'),
    path('отели_<str:city_name>', hotels_by_city, name='hotels_list'),
    path('hotel/<int:pk>/<str:slug>', HotelDetailView.as_view(), name='hotel_detail'),
    path('hotel/comment/<int:pk>', hotel_comment, name='hotel_comment'),
    path('hotel/ratings/<int:pk>', create_rating, name='rating_create'),
    path('hotel/order/<int:pk>', create_order, name='create_order')
]
