from rest_framework.views import APIView
from rest_framework.response import Response
from .tasks import get_routes


# endpoint view
class TransportApiView(APIView):
    def post(self, request, *args, **kwargs):
        payload = request.data['payload']
        data = get_routes.apply_async(args=(payload,))
        result = data.get()
        return Response(result)
