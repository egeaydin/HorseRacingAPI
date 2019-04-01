import json
import requests
from main.models import Result
from .celery import app
from celery.schedules import crontab
from main.enums import City
import time


@app.task(bind=True)
def gather(request):
    connect_timeout, read_timeout = 120, 120
    url_base = 'https://horseracingapi.herokuapp.com/race_day?year=2018&month=11&day=13&city={0}'
    for city in City:
        url = url_base.format(city.name)
        data = requests.get(url, timeout=(connect_timeout, read_timeout))

        if data.status_code == 200:
            data = json.loads(data.content.decode('utf-8'))
            for race in data.values():
                for result in race:
                    res = Result(**result)
                    res.save()
                    print('Race saved successfully')
        else:
            print('race did not exist')

        time.sleep(60)
