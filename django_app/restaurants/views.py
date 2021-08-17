from django.shortcuts import render
from .forms import RestaurantSearchForm

def main_page(request):
    context={'form': RestaurantSearchForm}
    return render(request, 'restaurants/main_page.html', context)

def result_page(request):
    if request.method == 'POST':
        form = RestaurantSearchForm(request.POST)
    context = {'form': form}
    return render(request, 'restaurants/result_page.html', context)
