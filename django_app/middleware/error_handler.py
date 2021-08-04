import requests
from django.http import HttpResponseRedirect
from django.contrib import messages
from hotels.utils.api_handler import CustomException
import logging


logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
file_handler = logging.FileHandler('exception.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.WARNING)


class BaseExceptionHandler():

    def __init__(self, get_response):
        self._get_response = get_response
        self.logger = logger

    def __call__(self, request):
        response = self._get_response(request)
        return response

    def process_exception(self, request, exception):
        logger.exception(exception)


class SpecialExceptionHandler(BaseExceptionHandler):

    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        response = self._get_response(request)
        return response

    def process_exception(self, request, exception):
        service = request.path.split('/')[1]
        if isinstance(exception, requests.exceptions.ConnectionError):
            messages.warning(request, 'Сервис временно не доступен')
            return HttpResponseRedirect(f'http://localhost:5000/{service}/main')
        if isinstance(exception, CustomException):
            messages.warning(request, exception)
            return HttpResponseRedirect(f'http://localhost:5000/{service}/main')
