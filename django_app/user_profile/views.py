from django.shortcuts import render, redirect
from .forms import UpdateNicknameForm, UpdateEmailForm, UpdatePasswordForm, UpdateForm
from django.contrib import messages


def change_data(request):
    form = UpdateForm()
    if request.method == 'POST':
        if 'Change Nickname' in request.POST:
            form = UpdateNicknameForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                form = UpdateForm()
                messages.success(request, f'Nickname has changed successfully for {request.user}')
            else:
                form = UpdateForm()
                messages.error(request, f'This nickname is used by another user.')
        elif 'Change Email' in request.POST:
            form = UpdateEmailForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                form = UpdateForm()
                messages.success(request, f'Email has changed successfully for {request.user}.')
            else:
                form = UpdateForm()
                messages.error(request, f'This email is used by another user.')
            
        elif 'Change Password' in request.POST:
            form = UpdatePasswordForm(request.user, request.POST)
            if form.is_valid():
                if form.cleaned_data.get('old_password') == form.cleaned_data.get('new_password1'):
                    messages.error(request, "Your old and new passwords are similar.")
                    form = UpdateForm()
                elif form.cleaned_data.get('new_password1') != form.cleaned_data.get('new_password2'):
                    messages.error(request, "Your new passwords isn't similar.")
                    form = UpdateForm()
                else:
                    form.save()
                    form = UpdateForm()
                    messages.success(request, f'Password has changed successfully for {request.user}.')
                    return redirect('user_auth:sign_in')
            else:
                messages.error(request, f"Your password is incorrect or new password can't be entirely numeric, can't be too similar to your personal information and must contain at least 8 characters.")
    context = {'form': form}
    return render(request, 'user_profile/user_profile.html', context)

def del_page(request):
    context = {}
    return render(request, 'user_profile/del_page.html', context)