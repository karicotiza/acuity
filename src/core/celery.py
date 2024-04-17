from os import environ
from celery import Celery  # type: ignore

environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app: Celery = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
