from django.urls import path

from . import views
app_name = 'user_auth'
urlpatterns = [
    path('', views.sign_up, name='sign_up'),
]
