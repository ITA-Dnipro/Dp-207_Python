from datetime import datetime
from subscription.models import Subscription, NotUniqueSubscription
import pytz


def create_subsciptions(post_dict, user):
    subscriptions = []
    if post_dict.get('weather'):
        service = 'weather'
        subscriptions.append(ServiceHandler().create_subsciption(post_dict, user, service))
    if post_dict.get('hotels'):
        service = 'hotels'
        subscriptions.append(ServiceHandler().create_subsciption(post_dict, user, service))
    if post_dict.get('transport'):
        service = 'transport'
        subscriptions.append(ServiceHandler().create_subsciption(post_dict, user, service))
    return subscriptions


class ServiceHandler():
    def __init__(self):
        self.model = Subscription

    def create_subsciption(self, post_dict, user, service):
        if service == 'transport':
            target_city = post_dict.get('city_of_arrival_for_transport')
            city_of_departure = post_dict.get('city_of_departure_for_transport')
        else:
            target_city = post_dict.get(f'city_for_{service}')
            city_of_departure = ''
        date_of_expire = post_dict.get(f'date_of_expire_for_{service}')
        date_of_expire = pytz.utc.localize(datetime.strptime(date_of_expire, '%Y-%m-%d'))
        try:
            subscription = self.model(target_city=target_city,
                                      city_of_departure=city_of_departure,
                                      date_of_expire=date_of_expire,
                                      service=service,
                                      user=user)
            subscription.save()
            return subscription
        except NotUniqueSubscription as e:
            return e

    def delete_subscription_by_id(self, pk):
        try:
            subscription = self.model.objects.get(pk=pk)
            subscription.delete()
            return True
        except self.model.DoesNotExist:
            return False

    def get_all_user_subscriptions(self, user_pk):
        subscriptions = self.model.objects.filter(user=user_pk)
        return subscriptions

    def get_by_id(self, pk):
        subscription = self.model.objects.get(pk=pk)
        return subscription
