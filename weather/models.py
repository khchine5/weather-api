from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from weather.enums import DetailingType
from weather.fields import CoordinateField


class WeatherForecast(models.Model):
    timestamp = models.DateTimeField(_("Datetime"), auto_now=True)
    data = models.JSONField(_("Forecast data"), default=dict)
    detailing_type = models.CharField(
        _("Detailing type"),
        max_length=10,
        choices=DetailingType.choices,
    )
    lat = CoordinateField(_("Latitude"))
    lon = CoordinateField(_("Longitude"))

    def __str__(self):
        return f"{self.timestamp} {self.detailing_type} {self.lat} {self.lon}"

    class meta:
        verbose_name = _("Weather forecast")
        verbose_name_plural = _("Weather forecasts")
        ordering = ("-timestamp",)

    @cached_property
    def is_valid(self):
        return (
            self.timestamp + timedelta(minutes=settings.WEATHER_API_LIFE_TIME_MINUTES)
            >= timezone.now()
        )
