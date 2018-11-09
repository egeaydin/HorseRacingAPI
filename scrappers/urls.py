from django.urls import path
from .views import FixtureView


urlpatterns = [
    path('fixture', FixtureView.as_view(), name='fixture'),
]
