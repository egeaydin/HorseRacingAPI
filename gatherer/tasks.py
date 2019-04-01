import json
import requests
from main.models import Result
import time


def debug_task(url):
    connect_timeout, read_timeout = 120, 120
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
