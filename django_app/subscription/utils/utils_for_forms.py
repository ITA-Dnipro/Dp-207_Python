from subscription.forms import UpdateTransportSubscriptionForm, UpdateHotelSubscriptionForm, UpdateWeatherSubscriptionForm


class ControllerForm():

    FORMS = {"weather": UpdateWeatherSubscriptionForm,
             "hotels": UpdateHotelSubscriptionForm,
             "transport": UpdateTransportSubscriptionForm}

    def __init__(self, subscription):
        self.subscription = subscription

    def get_proper_form(self):
        return self.FORMS[self.subscription.service]
