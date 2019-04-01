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
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1, day_of_month=1),
        debug_task.s(),
    )

# Load task modules from all registered Django app configs.
#app.autodiscover_tasks()




