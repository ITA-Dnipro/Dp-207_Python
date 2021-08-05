import os
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_SERVER_URL = os.environ.get('RABBITMQ_SERVER_URL')

broker_url = RABBITMQ_SERVER_URL
imports = (
    'services.statistics_app.celery_utils.celery_tasks.transport_app.transport_tasks_1',
)
