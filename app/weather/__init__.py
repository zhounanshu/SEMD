#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
from flask.ext.restful import Api

Weather = Blueprint('Weather', __name__)
weather_api = Api(Weather)

from .views import *
# weather_api.add_resource(viewRelti, '/v1/weather/realtime')
# weather_api.add_resource(viewForecast, '/v1/weather/forecast')
# weather_api.add_resource(alarm, '/v1/weather/alarm')
# weather_api.add_resource(rain, '/v1/weather/rain')
weather_api.add_resource(get_realtime, '/v1/weather/realtime')
weather_api.add_resource(get_forecast, '/v1/weather/forecast')
weather_api.add_resource(get_alarm, '/v1/weather/alarm')
weather_api.add_resource(get_rain, '/v1/weather/rain')