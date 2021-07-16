from django.urls import path

from . import views

app_name = 'transport'
urlpatterns = [
    path('list/', views.transport_list_view, name='transport_list'),
    path('form/', views.get_user_input, name='user_input'),
]
