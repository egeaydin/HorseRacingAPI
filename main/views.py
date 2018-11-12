from main.scrappers.page import FixtureScrapper, ResultScrapper
from .serializers import ResultSerializer
from .url_forms import RaceDayURLQueryForm
from rest_framework.response import Response
from rest_framework.views import APIView


class FixtureView(APIView):
    def get(self, request, format=None):
        query_params = RaceDayURLQueryForm(self.request.query_params)
        if query_params.is_valid():
            date = query_params.race_date
            city = query_params.cleaned_data['city']
            cache_key = city.value + date.timestamp()

            # First we check if result page is available for the race
            results = FixtureScrapper.scrap_by_date(city, date)

            race_day_dict = {}
            for i, race in enumerate(results):
                race_day_dict[i] = ResultSerializer(race, many=True).data
            return Response(race_day_dict)
        else:
            return Response(query_params.errors)
