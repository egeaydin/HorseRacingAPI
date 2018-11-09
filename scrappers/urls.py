from django.urls import path
from .views import fixture


urlpatterns = [
    path('fixture', fixture, name='fixture'),
]
