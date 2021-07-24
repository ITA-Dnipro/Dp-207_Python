from django.contrib import admin
from .models import City, Hotel, Rating, Order

admin.site.register(City)
admin.site.register(Hotel)
admin.site.register(Rating)
admin.site.register(Order)
