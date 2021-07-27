from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator
from .models import City, Hotel, HotelComment, Rating
from .forms import CityModelForm, HotelCommentCreateForm, RatingCreateForm, OrderCreateForm
from .utils.logic import CityAndHotelsHandler, CreateComment, CreateRating
from .utils.models_handler import HotelModel
from .utils.api_handler import get_for_hotel_rooms


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
    p = Paginator(sorted_hotels, 5)
    page_num = request.GET.get('page', 1)
    page = p.page(page_num)

    context = {
        'hotels': page
    }
    return render(request, 'hotels/hotels_list.html', context)


# hotel detail view
class HotelDetailView(DetailView):
    model = Hotel
    slug_url_kwarg = 'the_slug'
    slug_field = 'slug'
    pk_url_kwarg = 'pk'

    # get forms to context data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = HotelCommentCreateForm()
        context['rate'] = RatingCreateForm()
        context['order_form'] = OrderCreateForm()
        context['user'] = self.request.user
        context['check_rating'] = CreateRating(pk=self.object.pk, request=self.request)
        return context

    # override post method for check dates form validation
    def post(self, request, *args, **kwargs):
        order_form = OrderCreateForm(request.POST)
        if order_form.is_valid():
            self.object = self.get_object()
            check_in = order_form.cleaned_data['check_in'].date()
            check_out = order_form.cleaned_data['check_out'].date()
            return redirect('hotels:free_rooms', self.object.slug, check_in, check_out)
        else:
            self.object = self.get_object()
            context = super(HotelDetailView, self).get_context_data(**kwargs)
            context['order_form'] = order_form
            context['form'] = HotelCommentCreateForm()
            context['rate'] = RatingCreateForm()
            return self.render_to_response(context=context)


# create comments view
def hotel_comment(request, pk):
    new_comment = CreateComment(pk=pk, request=request)
    return HttpResponseRedirect(new_comment.create_comment().get_absolute_url())


# create rating mark for hotel
def create_rating(request, pk):
    new_rating = CreateRating(pk=pk, request=request)
    return HttpResponseRedirect(new_rating.create_rating().get_absolute_url())


def get_free_rooms_for_hotels(request, slug, check_in, check_out):
    hotel = HotelModel().get_hotel_by_slug(slug)
    print(type(hotel.city.name))

    check_in = '.'.join(check_in.split('-')[::-1])
    check_out = '.'.join(check_out.split('-')[::-1])
    print(check_in)
    data = get_for_hotel_rooms(hotel.city.name, hotel.name, check_in, check_out)
    print(data)
    return render(request, 'hotels/free_rooms.html', {'hotel': hotel})
