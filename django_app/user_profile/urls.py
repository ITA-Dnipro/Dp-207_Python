from django.urls import path
from . import views


app_name = 'user_profile'

urlpatterns = [
    path('', views.change_data, name='user_profile'),
    path('delete', views.del_page, name='del_page'),
    path('photo', views.change_photo, name='change_photo')
]
