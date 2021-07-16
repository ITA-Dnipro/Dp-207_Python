from django.shortcuts import render

from django.http import HttpResponse


def transport_list_view(request):
    return render(request, 'transport/transport.html')


def get_user_input(request):
    return render(request, 'transport/form.html')