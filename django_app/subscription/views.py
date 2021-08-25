from django.shortcuts import render
from .forms import SubscriptionForm #, SubscriptionHotelForm, SubscriptionWeatherForm, SubscriptionTransportForm
from subscription.utils.utils_for_views import find_period, create_subsciptions
from django.http import HttpResponseRedirect
from django.urls import reverse
from subscription.utils.api_handler import CityNotExists
from django.contrib import messages


def main(request):
    form = SubscriptionForm()
    # form_hotel = SubscriptionHotelForm()
    # form_weather = SubscriptionWeatherForm()
    # form_transport = SubscriptionTransportForm()
    # forms = {'hotel': form_hotel, 'weather': form_weather, 'transport': form_transport}
    if request.method == 'POST':
        print(request.user)
        print(create_subsciptions(post_dict=request.POST, user=request.user))
        # form = SubscriptionForm(request.POST)
        # if form.is_valid():
        #     period = find_period(request.POST.get('date_of_expire'))
        #     services = '?'.join(form.cleaned_data.get('services'))
        #     return HttpResponseRedirect(reverse('subscription:additional_form', args=(period, services)))
        return render(request, 'subscription/main_page.html', context={'form': form})
    return render(request, 'subscription/main_page.html', context={'form': form})


def choose_cities(request, period, services):
    class_form = AdditionalFormSetCreator(services.split('?')).create_form()
    form = class_form()
    if request.method == 'POST':
        form = class_form(request.POST)
        try:
            if form.is_valid():
                print(period)
                return render(request, 'subscription/additional_forms.html', context={'form': form, 'period': period, 'services': services})
        except CityNotExists as e:
            messages.warning(request, e.msg)

    return render(request, 'subscription/additional_forms.html', context={'form': form, 'period': period, 'services': services})
