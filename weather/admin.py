from django.contrib import admin
from jsoneditor.forms import JSONEditor
from django.db.models import JSONField
from .models import WeatherForecast


@admin.register(WeatherForecast)
class WeatherForecastAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "detailing_type", "lat", "lon")
    list_filter = ("timestamp", "detailing_type", "lat", "lon")
    search_fields = ("timestamp", "detailing_type", "lat", "lon")
    date_hierarchy = "timestamp"

    formfield_overrides = {
        JSONField: {
            "widget": JSONEditor(
                init_options={"mode": "view", "modes": ["view", "code", "tree"]},
                ace_options={"readOnly": True},
            )
        }
    }
