from django.urls import path
from . import views


app_name = 'transport'

urlpatterns = [
    path('', views.main_view, name='main_view'),
    path('<route_name>/', views.route_view, name='route_view'),
    path(
        'schedule',
        views.schedule_post_handler,
        name='schedule_post_handler'
    )

]
