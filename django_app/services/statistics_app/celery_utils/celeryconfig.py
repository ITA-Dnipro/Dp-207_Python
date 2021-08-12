import os
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_SERVER_URL = os.environ.get('RABBITMQ_SERVER_URL')

broker_url = RABBITMQ_SERVER_URL
imports = (
    'services.statistics_app.celery_utils.celery_tasks.transport_app.transport_tasks_1',
)
os.environ.setdefault('C_FORCE_ROOT', '1')
accept_content = ['pickle']
result_accept_content = ['pickle']
task_serializer = 'pickle'
result_serializer = 'pickle'
enable_utc = True
timezone = 'Europe/Kiev'
