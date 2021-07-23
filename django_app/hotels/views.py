from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.views.generic.detail import DetailView
from .models import City, Hotel, HotelComment, Rating
from .forms import CityModelForm, HotelCommentCreateForm, RatingCreateForm
from .logic import CityHotels


# create view for main page of hotels app
def main_page(request):
    # get sorted hotels by rating
    if request.method == 'POST':
        return redirect('hotels:hotels_list', request.POST.get('name').capitalize())
    hotels = sorted(Hotel.objects.all(), key=lambda x: -x.get_avg_marks())
    if hotels:
        return render(request, 'hotels/main_page.html',
                      {'form': CityModelForm(),
                       'hotels': hotels[:5]})
    return render(request, 'hotels/main_page.html', {'form': CityModelForm()})


# create view to get or create hotels by city search
def hotels_by_city(request, city_name):
    print(city_name)
    objects = CityHotels(city_name)
    # trying to get or create hotels raise warning if not
    if not objects.create_city_and_hotels():
        messages.warning(request, 'ТАКОГО ГОРОДА НЕТ')
        return redirect('hotels:main')
    else:
        objects.create_city_and_hotels()
        city = City.objects.filter(name=city_name).first()
        hotels = sorted(city.hotel_set.all(), key=lambda x: -x.get_avg_marks())
        context = {
            'hotels': hotels
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
        return context


# create comments view
def hotel_comment(request, pk):
    # get requested hotel by pk
    hotel = Hotel.objects.get(pk=pk)

    # create comment to this hotel
    try:
        text = request.POST.get('text')
        author = request.POST.get('author')
        if text and author:
            new_comment = HotelComment(
                hotel=hotel,
                text=text, author=author,
            )
            new_comment.save()
    except TypeError:
        print('Problem with creating new comment')
    finally:
        return HttpResponseRedirect(hotel.get_absolute_url())


# create rating mark for hotel
def create_rating(request, pk):
    # get requested hotel by pk
    hotel = Hotel.objects.get(pk=pk)

    # create mark
    try:
        mark = request.POST.get('mark')
        if mark:
            new_mark = Rating(
                hotel=hotel,
                mark=mark,
            )
            new_mark.save()
    except TypeError:
        print('Problem with creating new comment')
    finally:
        return HttpResponseRedirect(hotel.get_absolute_url())

def test(request):
    city = CityHotels('Киев')
    data = city.get_data_from_api()
    print(data)
    return render(request, 'hotels/test.html', {})