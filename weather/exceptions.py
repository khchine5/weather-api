from rest_framework.exceptions import APIException


class OpenWeatherAPIError(APIException):
    status_code = 400
    default_detail = "Error while getting weather forecast data from OpenWeather API"


class MissingAPIKey(APIException):
    status_code = 400
    default_detail = "OpenWeather API key is missing"
