from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from .models import Route
from .forms import JourneyDetailsForm
from .api_helper import Transport

import json
from .api_utils.api_request_helpers import create_api_call
import os


class TransportListView(ListView):
    model = Route



# def my_test_view(request):
#     payload = {
#         "departure_name": data['departure_name'],
#         "departure_date": data['arrival_name'],
#         "arrival_name": data['departure_date'],
#     }
#     TRANSPORT_APP_API_CARS_URL = os.environ.get('TRANSPORT_APP_API_CARS_URL')
#     api_response = create_api_call(payload, TRANSPORT_APP_API_CARS_URL)
#     context = json.loads(api_response.text)
#     print(context)
#     return render(request, 'transport/route_list.html', context=context)


def route_detales(request):
    departure_name = request.POST.get('departure_name')
    arrival_name = request.POST.get('arrival_name')
    departure_date = request.POST.get('departure_date')
    return render(request, "transport/form.html",
                  {"departure_name": departure_name,
                   "arrival_name": arrival_name,
                   "departure_date": departure_date})


def journey_details_view(request):
    form = JourneyDetailsForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            departure_name = request.POST.get('departure_name')
            arrival_name = request.POST.get('arrival_name')
            departure_date = request.POST.get('departure_date')
            routes = Transport(departure_name, arrival_name, departure_date)
            if not routes.create_route():
                return redirect(request, "transport/home.html")
            else:
                routes.create_route()
            return render(request, 'transport/route_list.html')
    else:
        form = JourneyDetailsForm()
    return render(request, "transport/route_form.html", {'form': form})

