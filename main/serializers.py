from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.utils.serializer_helpers import ReturnDict
from .models import Result


class ResultSerializer(ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'


