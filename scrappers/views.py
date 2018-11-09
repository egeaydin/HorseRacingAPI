from django.http import JsonResponse
from .page import FixtureScrapper
from .enums import City
from .serializers import FixtureSerializer
from django.core.cache import cache
from rest_framework.views import APIView
from datetime import datetime
from rest_framework.response import Response


class FixtureView(APIView):
    def get(self, request, format=None):
        date = datetime(2017, 11, 17)
        cache_key = City.Izmir.value + date.timestamp()

        # see if it is already cached
        fix = cache.get(cache_key)
        # if not cached
        if not fix:
            fix = cache.get_or_set(cache_key, FixtureScrapper.scrap_by_date(City.Izmir, date))

        return Response(FixtureSerializer(fix[1], many=True).data)
