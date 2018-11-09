# Horse Racing API
*API for getting horse race data from the official Turkish Jokey Organization!*

![alt text][banner]

Official Web site of Turkish Jokey Organization:[Turkish](http://www.tjk.org/)|[English](http://www.tjk.org/EN/YarisSever/YarisSever/Index)

## Installation Guide
Install the requirements with pip:
`pip install -r requirements.txt`

[banner]: github/banner.jpg "Horse Racing API banner"

## Caching
By default the data will be cached using django's filesystem caching.
To disable this comment out or delete these lines from base/settings.py file:
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': BASE_DIR,
    }
}
```
The cache files will be automatically created in the project directory. 
You can change this by changing ```LOCATION``` argument. 

If you want to use a different caching strategy follow [django's guide lines](https://docs.djangoproject.com/en/2.1/topics/cache/).