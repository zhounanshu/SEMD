#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
from flask.ext.restful import Api

Weather = Blueprint('Weather', __name__)
weather_api = Api(Weather)

from .views import *
# weather_api.add_resource(viewRelti, '/v1/weather/realtime')
# weather_api.add_resource(viewForecast, '/v1/wather/forecast')
weather_api.add_resource(alarm, '/v1/weather/alarm')
# weather_api.add_resource(rain, '/v1/weather/rain')
weather_api.add_resource(get_realtime, '/v1/weather/realtime')
weather_api.add_resource(get_forecast, '/v1/weather/forecast')
# weather_api.add_resource(get_alarm, '/v1/weather/alarm')
weather_api.add_resource(get_rain, '/v1/weather/rain')
# weather_api.add_resource(autoStation, '/v1/map/view/autostation')
weather_api.add_resource(get_qpf, '/v1/weather/qpf')
weather_api.add_resource(alarm_img, '/v1/alarm/img')
# upload weather station
weather_api.add_resource(realWether, '/v1/weather/realtime/upload')
weather_api.add_resource(realAqi, '/v1/aqi/realtime/upload')
weather_api.add_resource(foreWeat, '/v1/weather/forecast/upload')
weather_api.add_resource(wea_Station, '/v1/weather/station/upload')
# 根据经纬度自动定位
weather_api.add_resource(weatherLocation, '/v1/weather/location/realtime')
# 获取区县天气信息
weather_api.add_resource(get_disAla, '/v1/weather/area/alarm')
# 扫描区县天气情况
weather_api.add_resource(hasAlarm, '/v1/weather/has/alarm')
weather_api.add_resource(threeHour, '/v1/threehour/weather')
