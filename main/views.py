from main.scrappers.page import FixtureScrapper, ResultScrapper
from .url_forms import RaceDayURLQueryForm
from rest_framework.response import Response
from rest_framework.views import APIView
from .exception import PageDoesNotExist
from django.http import JsonResponse
from rest_framework import status


class RaceDayView(APIView):
    def get(self, request, format=None):
        query_params = RaceDayURLQueryForm(self.request.query_params)
        if query_params.is_valid():
            date = query_params.race_date
            city = query_params.cleaned_data['city']

            results = None
            # First we check if result page is available for the race
            try:
                results = ResultScrapper.scrap_by_date(city, date)
            except PageDoesNotExist:
                # No results found, let's see if there is fixture
                try:
                    results = FixtureScrapper.scrap_by_date(city, date)
                except PageDoesNotExist as page_does_not_exist:
                    # No fixture found either, that means no races happening in that city for the date
                    return Response(page_does_not_exist.full_details, status=status.HTTP_404_NOT_FOUND)

            return Response(results.serialize())
        else:
            return Response(query_params.errors)


def handler404(request, *args, **argv):
    return JsonResponse(
        {'Error': 'Requested url not found, please look at the tutorial: https://github.com/egeaydin/HorseRacingAPI#api-call',
         'status_code': 404})

