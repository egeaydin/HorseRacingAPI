from django.http import JsonResponse
from .page import FixtureScrapper
from .enums import City
from .serializers import FixtureSerializer
from django.core.cache import cache
from datetime import datetime


def fixture(request):
    date = datetime(2017, 11, 17)
    cache_key = City.Izmir.value + date.timestamp()

    # see if it is already cached
    fix = cache.get(cache_key)
    # if not cached
    if not fix:
        fix = cache.get_or_set(cache_key, FixtureScrapper.scrap_by_date(City.Izmir, date))
    return JsonResponse(FixtureSerializer(fix[0][0]).data)
