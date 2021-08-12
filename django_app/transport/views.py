import json
from datetime import datetime

from django.shortcuts import redirect, render
from services.transport_app.view_utils.view_helpers import get_route_data, create_user_dict

from .forms import RouteForm
from django.views.decorators.csrf import csrf_exempt
from services.statistics_app.celery_utils.celery_tasks.transport_app.transport_tasks_1 import (
    save_transport_data_to_mongo_db
)


def route_view(request, route_name):
    payload = json.loads(request.session.get('payload'))
    form = RouteForm()
    #
    route_data = get_route_data(payload)
    context = {
        'form': form,
        'cars_data': route_data.get('cars_data'),
        'trains_data': route_data.get('trains_data'),
    }
    #
    user_data = create_user_dict(user_data=request.user)
    #
    save_transport_data_to_mongo_db.apply_async(
        kwargs={'route_data': route_data, 'user_data': user_data},
        serializers='pickle'
    )
    #
    return render(
        request,
        'transport/route.html',
        context=context
    )


def main_view(request):
    if request.method == 'GET':
        form = RouteForm()
        return render(
            request,
            "transport/transport.html",
            context={'form': form},
        )

@csrf_exempt
def schedule_post_handler(request):
    if request.method == 'GET':
        return redirect(
            'transport:main_view',
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
            payload['departure_date'] = datetime.strftime(
                payload['departure_date'], '%d.%m.%Y'
            )
            request.session['payload'] = json.dumps(payload)
            return redirect(
                'transport:route_view',
                route_name=(
                        f'{payload["departure_name"]}-'
                        f'{payload["arrival_name"]}'
                    )
            )
        return redirect(
            'transport:main_view'
        )
