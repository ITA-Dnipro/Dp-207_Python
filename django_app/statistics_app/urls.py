from os import name
from django.urls import path
from . import views

app_name = 'statistics_app'

urlpatterns = [
    path('', views.stats_home, name='stats_home'),
    path('transport', views.transport_home, name='transport_home'),
    path('transport/<username>', views.user_page, name='user_page'),
    path(
        'user_page_form_handler',
        views.user_page_form_handler,
        name='user_page_form_handler'
    ),
    path(
        'route_page_form_handler/<username>',
        views.route_page_form_handler,
        name='route_page_form_handler'
    ),
    path(
        'transport/<username>/<route_name>',
        views.route_page,
        name='route_page'
    )
]
