from django.urls import path

from .views import TransportListView
from . import views


app_name = 'transport'
urlpatterns = [
    # path('list/', views.transport_list_view, name='transport_list'),
    path('list/', TransportListView.as_view(), name='transport_list'),
    path('form/', views.JourneyDetailsView.as_view(), name='user_input'),
]
