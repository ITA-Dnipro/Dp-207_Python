from django.urls import path
from . import views


app_name = 'restaurants'

urlpatterns = [
    path('main', views.main_page, name='main')
]