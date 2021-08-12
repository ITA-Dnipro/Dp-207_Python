from django.shortcuts import render
from django.contrib.admin.views.decorators import (
    staff_member_required
)
from services.statistics_app.view_utils.transport_app.view_helpers_1 import (
    get_last_20_users
)


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
    context = {}
    context['context_users'] = get_last_20_users()
    return render(request, 'statistics_app/transport_home.html', context=context)


@staff_member_required
def user_page(request, username):
    '''
    View func for '/statistics/transport/<username>' path
    '''
    return render(request, 'statistics_app/user_page.html', {})
