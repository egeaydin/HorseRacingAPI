from rest_framework.serializers import ModelSerializer
from .models.actual import Fixture


class FixtureSerializer(ModelSerializer):
    class Meta:
        model = Fixture
        fields = '__all__'


