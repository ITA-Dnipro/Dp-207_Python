from django.urls import path
from .views import main_page, hotels_by_city, HotelDetailView, \
    hotel_comment, create_rating


app_name = 'hotels'
urlpatterns = [
    path('main', main_page, name='main'),
    path('all', hotels_by_city, name='hotels_list'),
    path('hotel/<int:pk>', HotelDetailView.as_view(), name='hotel_detail'),
    path('hotel/comment/<int:pk>', hotel_comment, name='hotel_comment'),
    path('hotel/ratings/<int:pk>', create_rating, name='rating_create')
]
