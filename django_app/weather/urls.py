from django.urls import path
from . import views
from .api_views import WeatherApiView

app_name = "weather"

urlpatterns = [

    path('main', views.main_weather, name='main'),
    path('results/', views.get_weather_in_city, name='weather_info'),
    path('api/v1/get_weather', WeatherApiView.as_view(), name='api_weather'),
]
