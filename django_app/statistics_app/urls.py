from django.urls import path
from . import views

app_name = 'statistics_app'

urlpatterns = [
    path('', views.stats_home, name='stats_home')
]
