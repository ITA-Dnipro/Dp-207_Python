from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib import messages
from django.views.generic.detail import DetailView
from .models import City, Hotel, HotelComment, Rating
from .forms import CityModelForm, HotelCommentCreateForm, RatingCreateForm, OrderCreateForm
from .utils.logic import CityAndHotelsHandler, CreateComment, CreateRating
from .utils.models_handler import HotelModel


# create view for main page of hotels app
def main_page(request):
    # get sorted hotels by rating
    if request.method == 'POST':
        return redirect('hotels:hotels_list', request.POST.get('name').capitalize())

    # get sorted hotels by avg rating
    hotels = HotelModel().get_all_hotels()
    sorted_hotels = HotelModel().sort_hotels_by_avg_rating(reverse=True,
                                                           hotels=hotels)

    if sorted_hotels:
        return render(request, 'hotels/main_page.html',
                      {'form': CityModelForm(),
                       'hotels': sorted_hotels[:5]})
    return render(request, 'hotels/main_page.html', {'form': CityModelForm()})


# create view to get or create hotels by city search
def hotels_by_city(request, city_name):
    objects = CityAndHotelsHandler(city_name)

    if not objects.get_data_from_api_and_create_models():
        messages.warning(request, 'ТАКОГО ГОРОДА НЕТ')
        return redirect('hotels:main')
    objects.get_data_from_api_and_create_models()

    # get sorted hotels by avg rating
    hotels_in_city = HotelModel().get_all_hotels_by_city(city=city_name)
    sorted_hotels = HotelModel().sort_hotels_by_avg_rating(reverse=True,
                                                           hotels=hotels_in_city)
    context = {
        'hotels': sorted_hotels
    }
    return render(request, 'hotels/hotels_list.html', context)


# hotel detail view
class HotelDetailView(DetailView):
    model = Hotel

    # get forms to context data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = HotelCommentCreateForm()
        context['rate'] = RatingCreateForm()
        context['order_form'] = OrderCreateForm()
        return context


# create comments view
def hotel_comment(request, pk):
    new_comment = CreateComment(pk=pk, request=request)
    return HttpResponseRedirect(new_comment.create_comment().get_absolute_url())


# create rating mark for hotel
def create_rating(request, pk):
    new_rating = CreateRating(pk=pk, request=request)
    return HttpResponseRedirect(new_rating.create_rating().get_absolute_url())


def create_order(request, pk):
    # get requested hotel by pk
    hotel = Hotel.objects.get(pk=pk)
    try:
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        print(check_in, check_out)
    except TypeError:
        print('Problem with creating new comment')
    finally:
        return HttpResponseRedirect(hotel.get_absolute_url())