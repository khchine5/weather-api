import responses
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from freezegun import freeze_time
from responses import matchers
from rest_framework.test import APIClient

from weather.enums import DetailingType
from weather.models import WeatherForecast
from weather.services import OPEN_WEATHER_MAP_BASE_URL

SAMPLE_WEATHER_FORECAST_DATA = {
    "lat": 39.099724,
    "lon": -94.578331,
    "timezone": "America/Chicago",
    "timezone_offset": -18000,
    "current": {
        "dt": 1684929490,
        "sunrise": 1684926645,
        "sunset": 1684977332,
        "temp": 292.55,
        "feels_like": 292.87,
        "pressure": 1014,
        "humidity": 89,
        "dew_point": 290.69,
        "uvi": 0.16,
        "clouds": 53,
        "visibility": 10000,
        "wind_speed": 3.13,
        "wind_deg": 93,
        "wind_gust": 6.71,
        "weather": [
            {"id": 803, "main": "Clouds", "description": "broken clouds", "icon": "04d"}
        ],
    },
    "minutely": [
        {"dt": 1684929540, "precipitation": 0},
    ],
    "hourly": [
        {
            "dt": 1684926000,
            "temp": 292.01,
            "feels_like": 292.33,
            "pressure": 1014,
            "humidity": 91,
            "dew_point": 290.51,
            "uvi": 0,
            "clouds": 54,
            "visibility": 10000,
            "wind_speed": 2.58,
            "wind_deg": 86,
            "wind_gust": 5.88,
            "weather": [
                {
                    "id": 803,
                    "main": "Clouds",
                    "description": "broken clouds",
                    "icon": "04n",
                }
            ],
            "pop": 0.15,
        },
    ],
    "daily": [
        {
            "dt": 1684951200,
            "sunrise": 1684926645,
            "sunset": 1684977332,
            "moonrise": 1684941060,
            "moonset": 1684905480,
            "moon_phase": 0.16,
            "summary": "Expect a day of partly cloudy with rain",
            "temp": {
                "day": 299.03,
                "min": 290.69,
                "max": 300.35,
                "night": 291.45,
                "eve": 297.51,
                "morn": 292.55,
            },
            "feels_like": {
                "day": 299.21,
                "night": 291.37,
                "eve": 297.86,
                "morn": 292.87,
            },
            "pressure": 1016,
            "humidity": 59,
            "dew_point": 290.48,
            "wind_speed": 3.98,
            "wind_deg": 76,
            "wind_gust": 8.92,
            "weather": [
                {"id": 500, "main": "Rain", "description": "light rain", "icon": "10d"}
            ],
            "clouds": 92,
            "pop": 0.47,
            "rain": 0.15,
            "uvi": 9.23,
        },
    ],
    "alerts": [
        {
            "sender_name": "NWS Philadelphia - Mount Holly (New Jersey, Delaware, Southeastern Pennsylvania)",
            "event": "Small Craft Advisory",
            "start": 1684952747,
            "end": 1684988747,
            "description": """SMALL CRAFT ADVISORY REMAINS IN EFFECT FROM 5 PM THIS\nAFTERNOON TO 3 AM EST FRIDAY...\n*
            WHAT...North winds 15 to 20 kt with gusts up to 25 kt and seas\n3 to 5 ft expected.\n*
            WHERE...Coastal waters from Little Egg Inlet to Great Egg\n
            Inlet NJ out 20 nm, Coastal waters from Great Egg Inlet to\n
            Cape May NJ out 20 nm and Coastal waters from Manasquan Inlet\nto Little Egg Inlet NJ out 20 nm.\n*
            WHEN...From 5 PM this afternoon to 3 AM EST Friday.\n*
            IMPACTS...Conditions will be hazardous to small craft.""",
            "tags": [],
        },
    ],
}


class WeatherAppTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.weather_url = reverse("weather-api")

    def test_bad_endpoint_usage(self):
        lat = 39.099724
        lon = -94.578331
        open_weather_params = {
            "lat": lat,
            "lon": lon,
        }
        response = self.client.get(self.weather_url, data=open_weather_params)
        assert response.status_code == 400

    @responses.activate
    def test_weather_api_structure(self):
        lat = 39.099724
        lon = -94.578331
        open_weather_params = {
            "lat": lat,
            "lon": lon,
        }
        open_weather_response = responses.get(
            OPEN_WEATHER_MAP_BASE_URL,
            match=[
                matchers.query_param_matcher(open_weather_params, strict_match=False)
            ],
            json=SAMPLE_WEATHER_FORECAST_DATA,
        )

        assert WeatherForecast.objects.count() == 0

        # first request with hourly detailing type
        endpoint_hourly_params = {
            **open_weather_params,
            "detailing_type": DetailingType.HOURLY.value,
        }
        response = self.client.get(self.weather_url, data=endpoint_hourly_params)
        assert response.status_code == 200
        json_response = response.json()
        assert json_response["detailing_type"] == DetailingType.HOURLY.value
        assert json_response["lat"] == str(lat)
        assert json_response["lon"] == str(lon)
        assert json_response["data"] == SAMPLE_WEATHER_FORECAST_DATA["hourly"]
        assert WeatherForecast.objects.count() == 4
        assert open_weather_response.call_count == 1

    @responses.activate
    def test_weather_api(self):
        lat = 39.099724
        lon = -94.578331
        open_weather_params = {
            "lat": lat,
            "lon": lon,
        }
        open_weather_response = responses.get(
            OPEN_WEATHER_MAP_BASE_URL,
            match=[
                matchers.query_param_matcher(open_weather_params, strict_match=False)
            ],
            json=SAMPLE_WEATHER_FORECAST_DATA,
        )

        assert WeatherForecast.objects.count() == 0

        # first request with hourly detailing type
        endpoint_hourly_params = {
            **open_weather_params,
            "detailing_type": DetailingType.HOURLY.value,
        }
        endpoint_daily_params = {
            **open_weather_params,
            "detailing_type": DetailingType.DAILY.value,
        }
        response = self.client.get(self.weather_url, data=endpoint_hourly_params)
        assert response.status_code == 200
        assert WeatherForecast.objects.count() == 4
        assert open_weather_response.call_count == 1

        response = self.client.get(self.weather_url, data=endpoint_hourly_params)
        assert response.status_code == 200
        assert (
            open_weather_response.call_count == 1
        )  # no new call  because data is already in db

        # 11 minutes in the future
        with freeze_time(
            timezone.now()
            + timezone.timedelta(minutes=settings.WEATHER_API_LIFE_TIME_MINUTES + 1)
        ):
            # hourly
            response = self.client.get(self.weather_url, data=endpoint_hourly_params)
            assert response.status_code == 200
            assert open_weather_response.call_count == 2

        # 9 minutes in the future
        with freeze_time(
            timezone.now()
            + timezone.timedelta(minutes=settings.WEATHER_API_LIFE_TIME_MINUTES - 1)
        ):
            response = self.client.get(self.weather_url, data=endpoint_hourly_params)
            assert response.status_code == 200
            assert open_weather_response.call_count == 2

        # 9 minutes in the past
        with freeze_time(
            timezone.now()
            - timezone.timedelta(minutes=settings.WEATHER_API_LIFE_TIME_MINUTES - 1)
        ):
            response = self.client.get(self.weather_url, data=endpoint_hourly_params)
            assert response.status_code == 200
            assert open_weather_response.call_count == 2

        response = self.client.get(self.weather_url, data=endpoint_daily_params)
        assert response.status_code == 200
        assert (
            open_weather_response.call_count == 2
        )  # no new call because data is already in db even if detailing type is different
