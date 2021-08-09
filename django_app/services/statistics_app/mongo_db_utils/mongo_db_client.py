import os

from mongoengine import connect
from dotenv import load_dotenv

load_dotenv()

MONGO_DB_SERVICE_NAME = os.environ.get('MONGO_DB_SERVICE_NAME')
MONGO_DB_SERVICE_PORT = os.environ.get('MONGO_DB_SERVICE_PORT')
MONGO_INITDB_ROOT_USERNAME = os.environ.get('MONGO_INITDB_ROOT_USERNAME')
MONGO_INITDB_ROOT_PASSWORD = os.environ.get('MONGO_INITDB_ROOT_PASSWORD')


client = connect(
    db='transport_app',
    username=MONGO_INITDB_ROOT_USERNAME,
    password=MONGO_INITDB_ROOT_PASSWORD,
    authentication_source='admin',
    host=MONGO_DB_SERVICE_NAME,
    port=int(MONGO_DB_SERVICE_PORT),
    connect=False,
    alias='transport_app_alias'
)
