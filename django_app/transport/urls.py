from django.urls import path

from .views import TransportListView
from . import views


app_name = 'transport'
urlpatterns = [
    path('list/', TransportListView.as_view(), name='transport_list'),
    path('form/', views.journey_details_view, name='form_view'),
]
