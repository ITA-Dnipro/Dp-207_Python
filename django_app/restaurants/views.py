from django.shortcuts import render
from .forms import RestaurantSearchForm

def main_page(request):
    context={'form': RestaurantSearchForm}
    return render(request, 'restaurants/main_page.html', context)
