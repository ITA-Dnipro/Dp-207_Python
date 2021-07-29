from django.urls import path
from . import views

app_name = "weather"

urlpatterns = [

    path('main', views.main_weather, name='main'),
    path('results/', views.get_weather_in_city, name='weather_info'),
]
