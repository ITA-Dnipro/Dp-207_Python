from ..models import Weather
from .api_handler import get_weather_from_api
from datetime import timedelta
from django.utils import timezone


class WeatherHandler:
    """
    Class to control the way the weather data is provided
    """
    def __init__(self, city):
        self.city = city

    def create_weather_in_new_city(self):
        """
        If the city is not in Weather model, get data by API and add it in the model.
        """

        city = Weather.objects.filter(city=self.city).exists()
        if not city:
            try:
                weather_in_city = get_weather_from_api(self.city)

            except Exception:
                return False

            self.create_weather_in_city(weather_in_city)
        return True

    def get_weather_in_city_from_model(self):

        """
        If the data was created no longer than 1 hour from now, it is retrieved from Weather
        model. Otherwise, the 'old' data is deleted and 'new' one is added into the model.
        """

        time_limit = timezone.now() - timedelta(hours=1)
        result = Weather.objects.filter(city=self.city).filter(created__gt=time_limit)
        if result:
            weather_in_city = Weather.objects.filter(city=self.city).values()[0]
        else:
            self.delete_weather_in_city()
            weather_in_city = self.create_weather_in_city(get_weather_from_api(self.city))
        return weather_in_city

    def create_weather_in_city(self, data):
        """
        Add weather data into Weather model
        """

        weather_in_new_city = Weather.objects.create(
            temperature=data['temperature'],
            feels_like=data['feels_like'],
            description=data['description'],
            humidity=data['humidity'],
            wind=data['wind'],
            clouds=data['clouds'], city=self.city)
        weather_in_new_city.save()
        return weather_in_new_city

    def delete_weather_in_city(self):
        """
        Delete weather data from Weather model
        """
        Weather.objects.filter(city=self.city).delete()
        return True
