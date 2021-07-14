from django.shortcuts import render, redirect
from .forms import CreateUserForm

from django.contrib import messages


def sign_up(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f'Account was created for {user}')
            return redirect('user_auth:sign_up')
    context = {'form': form}
    return render(request, 'sign_up.html', context)
