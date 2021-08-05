from celery import Celery
from services.statistics_app.celery_utils import celeryconfig


app = Celery(main='statistics_celery')
app.config_from_object(celeryconfig)
