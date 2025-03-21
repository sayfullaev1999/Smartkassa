import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('smartkassa')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {

}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
