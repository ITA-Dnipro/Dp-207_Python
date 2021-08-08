import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_DB_SERVICE_NAME = os.environ.get('MONGO_DB_SERVICE_NAME')
MONGO_DB_SERVICE_PORT = os.environ.get('MONGO_DB_SERVICE_PORT')
MONGO_INITDB_ROOT_USERNAME = os.environ.get('MONGO_INITDB_ROOT_USERNAME')
MONGO_INITDB_ROOT_PASSWORD = os.environ.get('MONGO_INITDB_ROOT_PASSWORD')


client = MongoClient(
    f'mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@'
    f'{MONGO_DB_SERVICE_NAME}:{MONGO_DB_SERVICE_PORT}/',
    connect=False
)
