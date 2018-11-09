from django.http import JsonResponse
from .page import FixtureScrapper
from .enums import City
from .serializers import FixtureSerializer
from django.core.cache import cache
from datetime import datetime


def fixture(request):
    date = datetime(2017, 11, 17)
    fix = cache.get_or_set(City.Izmir.value + date.timestamp(), FixtureScrapper.scrap_by_date(City.Izmir, date))
    return JsonResponse(FixtureSerializer(fix[0][0]).data)
