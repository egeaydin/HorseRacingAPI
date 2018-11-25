from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

import requests
from celery.utils.log import get_task_logger

url = 'https://horseracingapi.herokuapp.com/race_day?year=2018&month=11&day=13&city=Adana'
logger = get_task_logger(__name__)

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gatherer.settings')

app = Celery()

#app.conf.beat_schedule = {
#    'add-every-30-seconds': {
#        'task': 'tasks.debug_task',
#        'schedule': 30.0,
#        'args': (16, 16)
#    },
#}
#app.conf.timezone = 'UTC'

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

import json

@app.task(bind=True)
def debug_task(self):
    from main.models import Result
    data = requests.get(url)
    data = json.loads(data.content.decode('utf-8'))

    for race in data.values():
        for result in race:
            res = Result(**result)
            res.save()



