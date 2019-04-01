import json
import requests
from main.models import Result
from .celery import app
from celery.schedules import crontab

'''
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, debug_task.s(), name='add every 10')
'''

@app.task(bind=True)
def gather(request):
    url = 'https://horseracingapi.herokuapp.com/race_day?year=2018&month=11&day=13&city=Izmir'
    data = requests.get(url)
    print(data.headers)
    data = json.loads(data.content.decode('utf-8'))
    print(data.values())

    for race in data.values():
        for result in race:
            res = Result(**result)
            res.save()
