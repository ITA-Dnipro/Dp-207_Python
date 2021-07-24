from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateUserForm


def home_page(request):
    return render(request, 'base.html')


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, f'Account was created for {user}')

                return redirect('user_auth:sign_in')

        context = {'form': form}
        return render(request, 'sign_up.html', context)


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('home')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Username or password isn't correct")

    context = {}
    return render(request, 'sign_in.html', context)


def sign_out(request):
    logout(request)
    return redirect('user_auth:sign_in')
