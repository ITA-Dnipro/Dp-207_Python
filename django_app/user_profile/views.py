from django.shortcuts import render
from .forms import UpdateNicknameForm, UpdateEmailForm, UpdatePasswordForm, UpdateForm


def change_data(request):
    form = UpdateForm()
    if request.method == 'POST':
        if 'Change Nickname' in request.POST:
            form = UpdateNicknameForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                form = UpdateForm()
        elif 'Change Email' in request.POST:
            form = UpdateEmailForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                form = UpdateForm()
        elif 'Change Password' in request.POST:
            form = UpdatePasswordForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                form = UpdateForm()
    context = {'form': form}
    return render(request, 'user_profile/user_profile.html', context)