from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import (
    staff_member_required
)
from services.statistics_app.view_utils.transport_app.view_helpers_1 import (
    get_last_20_users,
    get_users_count,
    get_user,
    get_20_routes_from_mongodb,
    get_routes_count,
    get_route_data,
)
from .forms import UserForm
from transport.forms import RouteForm
import json
from datetime import datetime
# import pytz


@staff_member_required
def stats_home(request):
    '''
    View func for '/statistics' path
    '''
    return render(request, 'statistics_app/statistics.html', {})


@staff_member_required
def transport_home(request):
    '''
    View func for '/statistics/transport' path
    '''
    form = UserForm()
    #
    context = {}
    context['context_users'] = get_last_20_users()
    context['context_users_count'] = get_users_count()
    context['form'] = form
    #
    return render(
        request,
        'statistics_app/transport_home.html',
        context=context,
    )


@staff_member_required
def user_page(request, username):
    '''
    View func for '/statistics/transport/<username>' path
    '''
    # payload = json.loads(request.session.get('payload'))
    context = {}
    context['context_routes'] = None
    mongo_user = get_user(username=username)
    if mongo_user:
        routes = get_20_routes_from_mongodb(user=mongo_user)
        context['context_routes'] = routes
    #
    context['context_user'] = mongo_user
    context['context_routes_count'] = get_routes_count(username=username)
    form = RouteForm()
    context['form'] = form
    return render(request, 'statistics_app/user_page.html', context=context)


def route_page(request, username, route_name):
    '''
    View func for '/statistics/transport/<username>/<route_name>' path
    '''
    payload = json.loads(request.session.get('payload'))
    context = {}
    context_route = get_route_data(
        username=username,
        payload=payload
    )
    mongo_user = get_user(username=username)
    context['context_route'] = context_route
    context['context_user'] = mongo_user
    return render(request, 'statistics_app/route_page.html', context=context)


def user_page_form_handler(request):
    '''
    View for POST form request
    '''
    if request.method == 'GET':
        return redirect(
            'statistics_app:transport_home',
        )
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            return redirect(
                'statistics_app:user_page',
                username=username
            )
        return redirect(
            'statistics_app:transport_home'
        )


def route_page_form_handler(request, username):
    '''
    View for POST form request
    '''
    if request.method == 'GET':
        return redirect(
            'statistics_app:transport_home',
        )
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            payload = {
                "departure_name": (
                    form.cleaned_data['departure_name'].lower().capitalize()
                ),
                "departure_date": form.cleaned_data['departure_date'],
                "arrival_name": (
                    form.cleaned_data['arrival_name'].lower().capitalize()
                ),
                "transport_types": form.cleaned_data['transport_types'],
            }
            #
            payload['departure_date'] = datetime.strftime(
                payload['departure_date'], '%d.%m.%Y'
            )
            request.session['payload'] = json.dumps(payload)
            return redirect(
                'statistics_app:route_page',
                username=username,
                route_name=(
                        f'{payload["departure_name"]}-'
                        f'{payload["arrival_name"]}'
                    )
            )
        return redirect(
            'statistics_app:transport_home'
        )
