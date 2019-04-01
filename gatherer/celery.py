from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from main.enums import City
from .tasks import debug_task

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

app = Celery()

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    url_base = 'https://horseracingapi.herokuapp.com/race_day?year=2018&month=11&day=13&city={0}'
    for city in City:
        debug_task.r(url_base.format(city.name))

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()




