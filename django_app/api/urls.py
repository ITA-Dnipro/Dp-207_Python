from django.urls import path
from .views import Cities


app_name = 'api'
urlpatterns = [
    path('get_all_cities', Cities.as_view(), name='get_cities')
]
