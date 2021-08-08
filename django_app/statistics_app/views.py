from django.shortcuts import render


def stats_home(request):
    '''
    View func for '/statistics' path
    '''
    return render(request, 'statistics_app/statistics.html', {})
