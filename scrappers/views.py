from django.http import HttpResponse


def fixture(request):
    return HttpResponse("Fixture will appear")
