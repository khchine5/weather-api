import json
from django.views.generic import TemplateView
from django.conf import settings
from .enums import DetailingType
from django.urls import reverse


class HomepageView(TemplateView):
    template_name = "weather/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Weather"
        context["config"] = json.dumps(
            {
                "GOOGLE_MAP_API_KEY": settings.GOOGLE_MAP_API_KEY,
                "DetailingTypeOptions": [
                    {"value": str(x[0]), "label": str(x[1])}
                    for x in DetailingType.choices
                ],
                "WEATHER_API_URL": reverse("weather-api"),
            }
        )
        return context
