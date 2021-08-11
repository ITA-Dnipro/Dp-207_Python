import requests
from django.http import HttpResponseRedirect
from django.contrib import messages
from hotels.utils.api_handler import CustomException
from loguru import logger
import os
import traceback


logger.add('exception.json', format='{time} - {level} - {message}',
           level='ERROR', rotation='10 MB', compression='zip', serialize=True)


class BaseExceptionHandler():

    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        response = self._get_response(request)
        return response

    def process_exception(self, request, exception):
        logger.error(traceback.format_exc())


class SpecialExceptionHandler(BaseExceptionHandler):

    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        response = self._get_response(request)
        return response

    def process_exception(self, request, exception):
        host = os.environ.get("ALLOWED_HOSTS").split(',')
        service = request.path.split('/')[1]
        if isinstance(exception, requests.exceptions.ConnectionError):
            messages.warning(request, 'Сервис временно не доступен')
            return HttpResponseRedirect(f'http://{host[1]}:5000/{service}/main')
        if isinstance(exception, CustomException):
            messages.warning(request, exception)
            return HttpResponseRedirect(f'http://{host[1]}:5000/{service}/main')
