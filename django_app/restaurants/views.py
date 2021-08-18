from django.shortcuts import render
from .forms import RestaurantSearchForm
from .utils import api_handler

def main_page(request):
    context={'form': RestaurantSearchForm}
    return render(request, 'restaurants/main_page.html', context)

def result_page(request):
    if request.method == 'POST':
        form = RestaurantSearchForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            restaurants = api_handler.get_restaurants_from_api(city=city)
    context = {'form': form, 'restaurants': restaurants}
    return render(request, 'restaurants/result_page.html', context)
