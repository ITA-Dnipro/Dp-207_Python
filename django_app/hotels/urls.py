from django.urls import path
from .views import *

#app_name = 'hotels'
urlpatterns = [
    path('', first, name = 'all_hotels'),

]