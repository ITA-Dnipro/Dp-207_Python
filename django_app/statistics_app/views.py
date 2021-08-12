from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import (
    staff_member_required
)
from services.statistics_app.view_utils.transport_app.view_helpers_1 import (
    get_last_20_users,
    get_users_count
)
from .forms import UserForm


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
    context['context_username'] = username
    return render(request, 'statistics_app/user_page.html', context=context)


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
