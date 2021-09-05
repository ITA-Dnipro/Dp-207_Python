from django.shortcuts import render, HttpResponseRedirect, redirect
from subscription.utils.utils_for_subscription import create_subsciptions, ServiceHandler
from django.contrib import messages
from subscription.models import NotUniqueSubscription
from subscription.utils.utils_for_forms import ControllerForm


def add(request):
    subscriptions = ServiceHandler().get_all_user_subscriptions(request.user.pk)
    if request.method == 'POST':
        subsciptions = create_subsciptions(post_dict=request.POST, user=request.user)
        for subsciption in subsciptions:
            if isinstance(subsciption, NotUniqueSubscription):
                messages.warning(request, subsciption)
            else:
                messages.success(request, f"{subsciption} was created")
        return HttpResponseRedirect('add')
    return render(request, 'subscription/add_subscription.html', {"subscriptions": subscriptions})


def delete(request, pk):
    ServiceHandler().delete_subscription_by_id(pk)
    return redirect('subscription:add_subscription')


def update(request, pk):
    subscription = ServiceHandler().get_by_id(pk)
    form = ControllerForm(subscription).get_proper_form()(instance=subscription)
    if request.method == 'POST':
        bound_form = ControllerForm(subscription).get_proper_form()(request.POST, instance=subscription)
        if bound_form.is_valid():
            update_subscription = bound_form.save(commit=False)
            print(update_subscription)
            update_subscription.update()
            return redirect('subscription:add_subscription')
        return render(request, 'subscription/update_subscription.html', {"form": bound_form, "subscription": subscription})
    return render(request, 'subscription/update_subscription.html', {"form": form, "subscription": subscription})
