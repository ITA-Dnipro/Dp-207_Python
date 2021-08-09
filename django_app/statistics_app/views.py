from django.shortcuts import render
from django.contrib.admin.views.decorators import (
    staff_member_required
)


@staff_member_required
def stats_home(request):
    '''
    View func for '/statistics' path
    '''
    return render(request, 'statistics_app/statistics.html', {})
