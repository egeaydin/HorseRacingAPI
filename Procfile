web: gunicorn main.wsgi --log-file -
celeryd: celery -A gatherer worker -E -B --loglevel=INFO