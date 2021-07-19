from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from .models import Route
from .forms import JourneyDetailsForm


import json
from .api_utils.api_request_helpers import create_api_call
import os


class TransportListView(ListView):
    model = Route


class JourneyDetailsView(FormView):
    template_name = 'transport/form.html'
    form_class = JourneyDetailsForm

    def form_valid(self, form):
        departure_place = form.cleaned_data['departure_name']
        arrival_place = form.cleaned_data['arrival_name']
        departure_day = form.cleaned_data['departure_date']
        return redirect('some_view_that_will_use_this_data', departure_place, arrival_place, departure_day)
