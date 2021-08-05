from rest_framework.views import APIView
from rest_framework.response import Response
from .tasks import get_weather


class WeatherApiView(APIView):
    def post(self, request, *args, **kwargs):
        city = request.data['city']
        data = get_weather.apply_async(args=(city,))
        result = data.get()
        return Response(result)
