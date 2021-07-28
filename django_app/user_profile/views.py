from django.shortcuts import render
from .forms import UpdateProfile


def change_data(request):
    form = UpdateProfile()
    if request.method == 'POST':
        form = UpdateProfile(request.POST, instance=request.user)
        print(form)
        if form.is_valid():
            form.save()
        else:
            form = UpdateProfile()
    context = {'form': form}
    return render(request, 'user_profile/user_profile.html', context)
