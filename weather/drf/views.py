from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from weather.drf.serializers import (
    WeatherForecastRequestSerializer,
    WeatherForecastSerializer,
)
from weather.services import weather_forecast_service


class WeatherForecastView(APIView):
    """
    Weather Forecast View
    """

    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        """
        Get weather forecast data
        """
        serializer = WeatherForecastRequestSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data
        # Get the weather forecast data
        weather_forecast_data = weather_forecast_service.get_weather_forecast_data(
            lag=validated_data["lat"],
            lon=validated_data["lon"],
            detail_type=validated_data["detailing_type"],
        )

        # Check if the weather forecast data is valid
        if weather_forecast_data["valid"]:
            # Return the weather forecast data
            forecast_serializer = WeatherForecastSerializer(
                weather_forecast_data["forecast"]
            )
            return Response(forecast_serializer.data, status=status.HTTP_200_OK)
        else:
            # Return the error message
            return Response(
                weather_forecast_data["error"], status=status.HTTP_400_BAD_REQUEST
            )
