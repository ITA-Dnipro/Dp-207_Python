from mongoengine.document import Document
from mongoengine.fields import (
    BooleanField, DateTimeField, EmailField, IntField, ReferenceField, StringField
)


class User(Document):
    username = StringField()
    #
    first_name = StringField()
    last_name = StringField()
    email = EmailField(unique=True)
    #
    is_active = BooleanField(default=False)
    is_staff = BooleanField(default=False)
    is_superuser = BooleanField(default=False)

    meta = {
        'db_alias': 'django_users_alias',
    }


class Route(Document):
    user = ReferenceField(User)
    #
    departure_name = StringField()
    arrival_name = StringField()
    departure_date = DateTimeField()
    parsed_time = DateTimeField()
    source_name = StringField()
    source_url = StringField()

    meta = {
        'db_alias': 'transport_app_alias',
        'allow_inheritance': True
    }


class Car(Document):
    route = ReferenceField(Route)
    #
    departure_name = StringField()
    departure_date = DateTimeField()
    #
    arrival_name = StringField()
    #
    price = StringField()
    car_model = StringField()
    blablacar_url = StringField()
    parsed_time = DateTimeField()
    source_name = StringField()
    source_url = StringField()

    meta = {
        'db_alias': 'transport_app_alias',
        'allow_inheritance': True
    }


class Train(Document):
    route = ReferenceField(Route)
    #
    train_name = StringField()
    train_number = StringField()
    train_uid = StringField()
    #
    departure_name = StringField()
    departure_code = IntField()
    departure_date = DateTimeField()
    #
    arrival_name = StringField()
    arrival_code = IntField()
    arrival_date = DateTimeField()
    #
    in_route_time = StringField()
    parsed_time = DateTimeField()
    source_name = StringField()
    source_url = StringField()

    meta = {
        'db_alias': 'transport_app_alias',
        'allow_inheritance': True
    }
