from ..models import Weather
from .api_handler import get_weather_from_api
from datetime import timedelta
from django.utils import timezone
from hotels.models import City


class WeatherHandler:
    """
     Class to control the way the weather data is provided
    """
    def __init__(self, city):
        self.city = city

    def get_weather_from_api_and_create_model(self):
        """
        If the city is not in Weather model, get data by API and add it in the model.
        """
        city_name = self.get_city_from_city_model()
        city = Weather.objects.filter(city=city_name).exists()
        if not city:
            try:
                weather_in_city = get_weather_from_api(self.city)
                forecast = weather_in_city['forecast']
            except Exception:
                return False
            for i in range(len(forecast)):
                self.create_weather_in_city(
                    current_temp=forecast[i]['current_temp'],
                    feels_like=forecast[i]['feels_like'],
                    description=forecast[i]['description'],
                    humidity=forecast[i]['humidity'],
                    wind=forecast[i]['wind'],
                    clouds=forecast[i]['clouds'],
                    max_temp=forecast[i]['max_temp'],
                    min_temp=forecast[i]['min_temp'],
                    current_date=forecast[i]['current_date'],
                    icon=forecast[i]['icon'])
        return True

    def create_weather_in_city(self, current_temp, feels_like, description,
                               humidity, wind, clouds, max_temp, min_temp,
                               current_date, icon ):
        """
        Add weather data into Weather model
        """
        c = self.get_city_from_city_model()
        weather_in_new_city = Weather(
            current_temp=current_temp,
            feels_like=feels_like,
            description=description,
            humidity=humidity,
            wind=wind,
            clouds=clouds,
            max_temp=max_temp,
            min_temp=min_temp,
            current_date=current_date,
            icon=icon,
            city=c)
        weather_in_new_city.save()
        return True

    def get_weather_from_model(self):
        city = self.get_city_from_city_model()
        return Weather.objects.filter(city=city).all()

    def get_city_from_city_model(self):
        return City.objects.get_or_create(name=self.city)[0]
