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

    def create_weather_in_new_city(self):
        """
        If the city is not in Weather model, get data by API and add it in the model.
        """
        c = self.get_city_from_city_model()
        city = Weather.objects.filter(city=c).exists()
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

        c = self.get_city_from_city_model()
        # time_limit = timezone.now() - timedelta(hours=1)
        # result = Weather.objects.filter(city=c).filter(created__gt=time_limit)
        result = Weather.objects.filter(city=c)
        if result:
            weather_in_city = Weather.objects.filter(city=c).values()
        else:
            # self.delete_weather_in_city()
            data = get_weather_from_api(self.city)
            weather_in_city = self.create_weather_in_city(data)
        return weather_in_city

    def create_weather_in_city(self, data):
        """
        Add weather data into Weather model
        """
        c = self.get_city_from_city_model()
        forecast = data['forecast']
        for i in range(len(forecast)):
            weather_in_new_city = Weather(
                current_temp=forecast[i]['current_temp'],
                feels_like=forecast[i]['feels_like'],
                description=forecast[i]['description'],
                humidity=forecast[i]['humidity'],
                wind=forecast[i]['wind'],
                clouds=forecast[i]['clouds'],
                max_temp=forecast[i]['max_temp'],
                min_temp=forecast[i]['min_temp'],
                current_date=forecast[i]['current_date'],
                icon=forecast[i]['icon'],
                city=c)
            weather_in_new_city.save()
        return forecast

    def delete_weather_in_city(self):
        """
        Delete weather data from Weather model
        """
        c = self.get_city_from_city_model()
        Weather.objects.filter(city=c).delete()
        return True

    def get_city_from_city_model(self):
        return City.objects.get_or_create(name=self.city)[0]
