from django.urls import path
from .views import add, update, delete
from django.conf.urls.static import static
from django.conf import settings


app_name = "subscription"

urlpatterns = [
        path('add', add, name='add_subscription'),
        path('update/<int:pk>', update, name='update_subscription'),
        path('delete/<int:pk>', delete, name='delete_subscription'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
