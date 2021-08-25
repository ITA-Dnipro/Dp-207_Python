from django.urls import path
from .views import main, choose_cities
from django.conf.urls.static import static
from django.conf import settings


app_name = "subscription"

urlpatterns = [
        path('main', main, name='main'),
        path('additional-form/?period=<int:period>/?services=<str:services>', choose_cities, name='additional_form'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)