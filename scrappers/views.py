from .page import FixtureScrapper
from .enums import City
from .serializers import FixtureSerializer
from .url_forms import RaceDayURLQueryForm
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView


class FixtureView(APIView):
    def get(self, request, format=None):
        query_params = RaceDayURLQueryForm(self.request.query_params)
        if query_params.is_valid():
            date = query_params.race_date
            city = query_params.cleaned_data['city']
            cache_key = city.value + date.timestamp()

            # see if it is already cached
            fix = cache.get(cache_key)
            # if not cached
            if not fix:
                fix = cache.get_or_set(cache_key, FixtureScrapper.scrap_by_date(city, date))

            return Response(self.fixture_to_race_day(fix))
        else:
            return Response(query_params.errors)

    def fixture_to_race_day(self, fix):
        race_day_dict = {}
        for i, race in enumerate(fix):
            race_day_dict[i] = FixtureSerializer(race, many=True).data
        return race_day_dict
