import requests
from django.conf import settings

from weather.enums import DetailingType
from weather.exceptions import MissingAPIKey, OpenWeatherAPIError
from weather.models import WeatherForecast

OPEN_WEATHER_MAP_BASE_URL = "https://api.openweathermap.org/data/2.5/onecall"


class WeatherForecastService:
    def __init__(self):
        if not settings.WEATHER_API_KEY:
            raise MissingAPIKey()
        self.weather_api_key = settings.WEATHER_API_KEY

    def get_weather_forecast(self, lat, lon):
        weather_forecast_data = requests.get(
            OPEN_WEATHER_MAP_BASE_URL,
            params={"lat": lat, "lon": lon, "appid": self.weather_api_key},
        )
        if weather_forecast_data.ok:
            return weather_forecast_data.json()
        else:
            raise OpenWeatherAPIError()

    def get_weather_forecast_data(self, lag, lon, detail_type):
        forecast = WeatherForecast.objects.filter(
            lat=lag, lon=lon, detailing_type=detail_type
        ).first()  # sort by timestamp
        if not forecast or (forecast and not forecast.is_valid):
            weather_forecast_data = self.get_weather_forecast(lag, lon)
            if weather_forecast_data:
                for (
                    api_detail_type
                ) in DetailingType.values:  # loop through all detailing types
                    if api_detail_type_data := weather_forecast_data.get(
                        api_detail_type
                    ):
                        if (
                            forecast
                            and forecast.detailing_type == api_detail_type
                            and forecast.data != api_detail_type_data
                        ):
                            forecast.data = api_detail_type_data
                            forecast.save()
                        else:
                            # create new forecast even if it exists but with different detailing type
                            # this will save a new API request for the same coordinates but different detailing type
                            WeatherForecast.objects.create(
                                lat=lag,
                                lon=lon,
                                detailing_type=api_detail_type,
                                data=api_detail_type_data,
                            )
                forecast = WeatherForecast.objects.filter(
                    lat=lag, lon=lon, detailing_type=detail_type
                ).first()
            else:
                return {
                    "valid": False,
                    "error": "Error while getting weather forecast data from API",
                }
        return {"valid": True, "forecast": forecast}


weather_forecast_service = WeatherForecastService()
