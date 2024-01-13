from django.urls import path
from weather.views import HomepageView
from weather.drf.views import WeatherForecastView

urlpatterns = [
    path("weather-api", WeatherForecastView.as_view(), name="weather-api"),
    path("", HomepageView.as_view(), name="index"),
]
