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
    )
]
