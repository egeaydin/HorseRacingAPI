import json
import requests
from main.models import Result
from .celery import app


@app.task(bind=True)
def debug_task(request):
    url = 'https://horseracingapi.herokuapp.com/race_day?year=2018&month=11&day=13&city=Adana'
    data = requests.get(url)
    data = json.loads(data.content.decode('utf-8'))

    for race in data.values():
        for result in race:
            res = Result(**result)
            res.save()
