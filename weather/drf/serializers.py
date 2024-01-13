from rest_framework import serializers

from weather.enums import DetailingType
from weather.models import WeatherForecast


class WeatherForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherForecast
        fields = ["data", "detailing_type", "lat", "lon"]


class WeatherForecastRequestSerializer(serializers.Serializer):
    lat = serializers.DecimalField(max_digits=9, decimal_places=6)
    lon = serializers.DecimalField(max_digits=9, decimal_places=6)
    detailing_type = serializers.ChoiceField(choices=DetailingType.values)
