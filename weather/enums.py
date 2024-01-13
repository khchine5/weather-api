from django.db import models
from django.utils.translation import gettext_lazy as _


class DetailingType(models.TextChoices):
    CURRENT = "current", _("Current")
    MINUTELY = "minutely", _("Minutely")
    HOURLY = "hourly", _("Hourly")
    DAILY = "daily", _("Daily")
